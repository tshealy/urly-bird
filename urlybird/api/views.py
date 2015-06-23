from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .serializers import BookmarkSerializer, ClickSerializer
from bookmark.models import Bookmark
from click.models import Click
from .permissions import IsOwnerOrReadOnly, OwnsRelatedBookmark
from rest_framework.exceptions import PermissionDenied
# Create your views here.

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset= Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
          serializer.save(user=self.request.user)


class ClickList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = ClickSerializer

    def get_queryset(self):
        bookmarkpk = self.kwargs['pk']
        clicks = Click.objects.filter(bookmark__pk = bookmarkpk)
        return clicks

    def perform_create(self, serializer):
          serializer.save(user=self.request.user)

class ClickCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClickSerializer

    def perform_create(self, serializer):
        bookmark = serializer.validated_data['bookmark']
        if self.request.user != bookmark.user:
            raise PermissionDenied
        serializer.save()


class ClickDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,
                          OwnsRelatedBookmark)
    serializer_class = ClickSerializer
    queryset = Click.objects.all()