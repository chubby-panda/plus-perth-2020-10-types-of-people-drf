from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    is_org = models.BooleanField('is organisation', default=False)

    def __str__(self):
        return str(self.username)


class MentorProfile(models.Model):
    name = models.CharField(max_length=300, blank=True)
    bio = models.CharField(max_length=5000, blank=True)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='mentor_profile',
    )

    def __str__(self):
        return self.user.username

   
class OrgProfile(models.Model):
    company_name = models.CharField(max_length=300, blank=True)
    contact_name = models.CharField(max_length=300, blank=True)
    org_bio = models.CharField(max_length=5000, blank=True)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='org_profile',
    )

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_org:
            OrgProfile.objects.create(user=instance)
        else:
            MentorProfile.objects.create(user=instance)


# @receiver(post_save, sender=CustomUser)
# def update_profile(sender, instance, created, **kwargs):
#     if created == False:
#         if instance.is_org:
#             instance.OrgProfile.save()
#         else:
#             instance.MentorProfile.save()

###why not one function? ###