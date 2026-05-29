from django.contrib import admin

from .models import Project, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'status', 'created_at')
    list_filter = ('status', 'skills')
    search_fields = ('name', 'description')
