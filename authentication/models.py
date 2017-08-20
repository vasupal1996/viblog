from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import pre_save, post_save

from post.models import  Tag


def image_upload_location(instance, filename):
    user = instance.user
    pk = instance.pk
    profile = 'profile'
    return "%s/%s/%s" %(user,profile,filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.ImageField(upload_to = image_upload_location)
    dob = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.IntegerField(blank=True, null=True)
    alternate_email = models.EmailField(blank=True, null=True)
    intro_slogan = models.CharField(max_length=75, null=True, blank=True)

    def __str__(self):
        return str(self.user)    


    def get_profile_image(self):
        image = self.profile_image
        image = image.url
        return image

def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def save_user_profile(sender, instance, *args, **kwargs):
    instance.userprofile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)