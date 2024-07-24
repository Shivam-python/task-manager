from rest_framework import viewsets
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project')
        if project:
            queryset = queryset.filter(project_id=project)
        return queryset

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
