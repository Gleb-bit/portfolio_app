from django.contrib import admin

from projects.models import Project


class ProjectsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectsAdmin)
