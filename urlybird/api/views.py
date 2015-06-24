from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, filters
from .serializers import BookmarkSerializer, ClickSerializer, UserSerializer
from bookmark.models import Bookmark
from click.models import Click
from .permissions import IsOwnerOrReadOnly, OwnsRelatedBookmark
from rest_framework.exceptions import PermissionDenied
import django_filters
from django.contrib.auth.models import User


# Create your views here.

class BookmarkFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(name='title', lookup_type='icontains')
    long = django_filters.CharFilter(name='long', lookup_type='icontains')
    description = django_filters.CharFilter(name='description', lookup_type='icontains')

    class Meta:
        model = Bookmark
        fields = ['title', 'long', 'description']

class BookmarkViewSet(viewsets.ModelViewSet):
    # queryset= Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BookmarkFilter

    def get_queryset(self):
        return Bookmark.objects.filter(user = self.request.user)

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


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateView(generics.CreateAPIView):
    # permission_classes = (permissions.IsAuthenticated)
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()