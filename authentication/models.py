from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import pre_save, post_save

def image_upload_location(instance, filename):
    user = instance.user
    pk = instance.pk
    profile = 'profile-images'
    return "%s/%s/%s" %(profile, user, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.ImageField(upload_to = image_upload_location)
    dob = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.IntegerField(blank=True, null=True)
    alternate_email = models.EmailField(blank=True, null=True)
    #intro_slogan = models.CharField(max_length=75, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    # def get_profile_url(self):
    #     try:
    #         if self.url:
    #             if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
    #                 return "https://"+ str(self.url)
    #     except Exception:
    #         return "https://"+ str(self.user.username)

    def get_profile_picture_url(self):
        try:
            if self.profile_image:
                profile_picture = (self.profile_image).url
                return profile_picture
            else:
                profile_picture = 'https://d30y9cdsu7xlg0.cloudfront.net/png/363633-200.png'
                return profile_picture
        except Exception:
            return 'https://d30y9cdsu7xlg0.cloudfront.net/png/363633-200.png'
        
    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except Exception:
            return self.user.username

def create_user_profile(sender, instance, created, *args, **kwargs):
    try:
        if created:
            UserProfile.objects.create(user=instance)
    except Exception:
        pass

def save_user_profile(sender, instance, *args, **kwargs):
    try:
        instance.userprofile.save()
    except Exception:
        pass

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
