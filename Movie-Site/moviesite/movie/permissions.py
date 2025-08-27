from rest_framework import permissions
from .models import Movie

class CheckMovie(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
           if request.user.status == obj.status:
               return True
           elif request.user.status == 'pro':
               return True





