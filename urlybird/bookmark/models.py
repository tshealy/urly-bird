from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime


class Bookmark(models.Model):
    user = models.ForeignKey(User)
    long = models.URLField(max_length=255)
    short = models.CharField(max_length=255, null=True, blank=True) #should this be a function?
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True)

    def get_absolute_url(self):
        return reverse('/index/', kwargs={'pk': self.pk})
#send to bookmark detail

    def total_clicks(self):
        # return len(self.click_set.all())
        return self.click_set.count()
