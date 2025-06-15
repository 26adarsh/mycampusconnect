# signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Only create UserProfile without hardcoding role
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            pass
