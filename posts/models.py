from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from groups.models import Group
from geoposition.fields import GeopositionField

from cloudinary.models import CloudinaryField

User = get_user_model()

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    #profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    profile_pic = CloudinaryField(resource_type='auto')
    position = GeopositionField(null=True)
    group = models.ForeignKey(
        Group, related_name='posts', on_delete=models.CASCADE,
        blank=True, null=True)


    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = self.message
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'posts:single',
            kwargs={
                'username': self.user.username,
                'pk': self.pk
            }
        )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message', 'created_at']
