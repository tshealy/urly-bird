from rest_framework import serializers
from bookmark.models import Bookmark
from click.models import Click



class ClickSerializer(serializers.HyperlinkedModelSerializer):
    # bookmark = BookmarkSerializer(many=True, read_only=True)
    class Meta:
        model = Click
        fields = ('bookmark', 'time', 'address', 'browser', 'user')

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
     user = serializers.PrimaryKeyRelatedField(read_only=True)
     # click = ClickSerializer(many=True, read_only=True)
     click = serializers.HyperlinkedIdentityField(view_name='click-list')
     # id = serializers.HyperlinkedIdentityField(view_name='id')
     class Meta:
         model = Bookmark
         fields = ('user', 'title', 'description', 'long', 'short', 'created', 'edited',  'click', 'total_clicks')


