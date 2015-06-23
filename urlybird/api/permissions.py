from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
               #checking for ownership
          if request.method in permissions.SAFE_METHODS:
               return True
          else:
               return request.user == obj.user

class OwnsRelatedBookmark(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.bookmark.user