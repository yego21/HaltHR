from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Department
import sys
from django.contrib.auth.models import Group

# Global variable to store previous department_head
previous_department_head = None


@receiver(pre_save, sender=Department)
def capture_previous_department_head(sender, instance, **kwargs):
    global previous_department_head
    if instance.pk:
        # Fetch the old department_head if the instance exists in the database
        try:
            old_instance = Department.objects.get(pk=instance.pk)
            previous_department_head = old_instance.department_head
        except Department.DoesNotExist:
            previous_department_head = None
    else:
        # New instance being created, no previous department_head
        previous_department_head = None


@receiver(post_save, sender=Department)
def update_user_staff_status(sender, instance, **kwargs):
    global previous_department_head
    print(f'Handling staff status for User: {instance}', file=sys.stdout, flush=True)
    department_heads_group, created = Group.objects.get_or_create(name='Department Heads')

    if previous_department_head:
        if previous_department_head != instance.department_head:
            # Update previous department_head's is_staff status
            previous_department_head.user.is_staff = False
            previous_department_head.user.groups.remove(department_heads_group)
            previous_department_head.user.save()

    if instance.department_head:
        # Update current department_head's is_staff status
        instance.department_head.user.is_staff = True
        instance.department_head.user.groups.add(department_heads_group)
        instance.department_head.user.save()

    # Reset the global variable after processing
    previous_department_head = None
