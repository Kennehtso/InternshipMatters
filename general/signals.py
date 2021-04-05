from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import InternPerson

def internPerson_profile(sender, instance, created, **kwargs):
    if created:
        # Add New user to group 'InternPerson'
        group = Group.objects.get(name='internPerson')
        instance.groups.add(group)
        
        # create InternPerson when create User
        # Due to already set One To One relationship in model, so we can do as:
        InternPerson.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )
        print(f"profile created")
post_save.connect(internPerson_profile, sender=User)