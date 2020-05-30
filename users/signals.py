from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Profile
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_profile(instance,sender,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(instance,sender,**kwargs):
    instance.profile.save()