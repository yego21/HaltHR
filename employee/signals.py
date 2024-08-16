from django.dispatch import Signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from company.models import Department
import sys

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    print(f'Creating userprofile for User: {instance}', file=sys.stdout, flush=True)
    if created:
        # Create UserProfile if it doesn't already exist
        UserProfile.objects.get_or_create(user=instance)
    else:
        # Ensure UserProfile is saved if it already exists
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# @receiver(post_save, sender=UserProfile)
# def update_user_staff_status(sender, instance, **kwargs):
#     print(f'Handling staff status for User: {instance}', file=sys.stdout, flush=True)
#     if hasattr(instance, 'staff_handling'):
#         return instance.staff_handling
#
#     instance.user.save()

# @receiver(post_save, sender=User)
# def manage_user_shift(sender, instance, created, **kwargs):
#     if created:
#         # Create UserProfile if it doesn't already exist
#         UserShift.objects.get_or_create(user=instance)
#     else:
#         # Ensure UserProfile is saved if it already exists
#         if hasattr(instance, 'usershift'):
#             instance.usershift.save()
#
# @receiver(post_save, sender=User)
# def save_user_shift(sender, instance, **kwargs):
#     instance.usershift.save()
