from http import HTTPStatus

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Project, Skill


PAGINATE_BY = 12
SKILL_AUTOCOMPLETE_LIMIT = 10
PROJECT_STATUS_OPEN = Project.STATUS_OPEN
PROJECT_STATUS_CLOSED = Project.STATUS_CLOSED


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        qs = Project.objects.filter(status=PROJECT_STATUS_OPEN).select_related(
            'owner'
        )
        skill_name = self.request.GET.get('skill')
        if skill_name:
            qs = qs.filter(skills__name=skill_name)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_skills'] = Skill.objects.all().order_by('name')
        context['active_skill'] = self.request.GET.get('skill')
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description', 'github_url', 'status']
    template_name = 'projects/create-project.html'
    success_url = reverse_lazy('projects:project_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        project = form.save()
        project.participants.add(self.request.user)
        return redirect('projects:project_detail', pk=project.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'description', 'github_url', 'status']
    template_name = 'projects/create-project.html'
    success_url = reverse_lazy('projects:project_list')

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            return redirect('projects:project_detail', pk=project.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


@login_required
@require_POST
def project_complete(request, pk):
    try:
        project = Project.objects.get(pk=pk, owner=request.user)
    except Project.DoesNotExist:
        return JsonResponse(
            {'error': 'Project not found'}, status=HTTPStatus.NOT_FOUND
        )

    project.status = PROJECT_STATUS_CLOSED
    project.save()
    return JsonResponse(
        {'status': 'ok', 'project_status': PROJECT_STATUS_CLOSED}
    )


@login_required
@require_POST
def toggle_participate(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return JsonResponse(
            {'error': 'Project not found'}, status=HTTPStatus.NOT_FOUND
        )

    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({'status': 'ok'})


def skill_autocomplete(request):
    search_term = request.GET.get('q', '')
    skills = Skill.objects.filter(
        name__istartswith=search_term
        ).order_by('name')[
        :SKILL_AUTOCOMPLETE_LIMIT
    ]
    skills_data = [{'id': skill.id, 'name': skill.name} for skill in skills]
    return JsonResponse(skills_data, safe=False)


@login_required
@require_POST
def add_skill_to_project(request, pk):
    try:
        project = Project.objects.get(pk=pk, owner=request.user)
    except Project.DoesNotExist:
        return JsonResponse(
            {'error': 'Project not found'}, status=HTTPStatus.NOT_FOUND
        )

    skill_name = request.POST.get('name')
    if not skill_name:
        return JsonResponse(
            {'error': 'Skill name is required'},
            status=HTTPStatus.BAD_REQUEST
        )

    skill, created = Skill.objects.get_or_create(name=skill_name)
    if project.skills.filter(pk=skill.pk).exists():
        return JsonResponse({'skill_id': skill.id, 'added': False})
    project.skills.add(skill)
    return JsonResponse({
        'skill_id': skill.id,
        'added': True,
        'created': created
    })


@login_required
@require_POST
def remove_skill_from_project(request, project_pk, skill_pk):
    try:
        project = Project.objects.get(pk=project_pk, owner=request.user)
    except Project.DoesNotExist:
        return JsonResponse(
            {'error': 'Project not found'}, status=HTTPStatus.NOT_FOUND
        )

    try:
        skill = Skill.objects.get(pk=skill_pk)
    except Skill.DoesNotExist:
        return JsonResponse(
            {'error': 'Skill not found'}, status=HTTPStatus.NOT_FOUND
        )

    project.skills.remove(skill)
    return JsonResponse({'status': 'ok'})
