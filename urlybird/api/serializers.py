from rest_framework import serializers
from bookmark.models import Bookmark
from click.models import Click
from hashids import Hashids
from django.contrib.auth.models import User

class ClickSerializer(serializers.HyperlinkedModelSerializer):
    # bookmark = BookmarkSerializer(many=True, read_only=True)
    class Meta:
        model = Click
        fields = ('bookmark', 'time', 'address', 'browser', 'user')

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
     user = serializers.PrimaryKeyRelatedField(read_only=True)
     click = serializers.HyperlinkedIdentityField(view_name='click-list')
     # url = serializers.HyperlinkedIdentityField(view_name='bookmark-detail')
     short = serializers.CharField(read_only=True)

     def create(self, validated_data):
         hashids = Hashids(min_length = 4, salt="browndogbella")
         previous = Bookmark.objects.latest('id')
         previousid = previous.id
         if previous.id is None:
             previousid = 0
         bookmark = Bookmark.objects.create(**validated_data)
         bookmark.short = hashids.encrypt(previousid + 1)
         bookmark.save()
         return bookmark


     class Meta:
         model = Bookmark
         fields = ('id', 'user', 'title', 'description', 'url', 'long', 'short', 'created', 'edited',  'click', 'total_clicks')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')