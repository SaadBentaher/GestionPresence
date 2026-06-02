from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Membership


@receiver(post_save, sender=Membership)
def membership_post_save(sender, instance, created, **kwargs):
    pass
