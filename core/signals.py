from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Automatically create UserProfile when a new User is created
        UserProfile.objects.create(user=instance, role='student')
    else:
        # Update profile if user is updated
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            pass  # Or optionally create: UserProfile.objects.create(user=instance, role='student')
