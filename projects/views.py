from django.views import generic
from projects.models import Project
from django.views import generic

from projects.models import Project


class ListProjectView(generic.ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'project_index.html'


class DetailProjectView(generic.DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'project_detail.html'
