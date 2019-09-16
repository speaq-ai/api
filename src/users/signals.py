from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.serializers import ProfileSerializer


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if not created:
        return

    profile_serializer = ProfileSerializer(data={"user": instance.id})
    if profile_serializer.is_valid():
        profile_serializer.save()
    else:
        print(profile_serializer.errors)
