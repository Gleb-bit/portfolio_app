from django.shortcuts import render
from django.views import generic

from projects.models import Project


class ListProjectView(generic.ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'list_project.html'


class DetailProjectView(generic.DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'detail_project.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        context = {'project': Project.objects.filter(pk=pk)[0]}
        return render(request, self.template_name, (context))
