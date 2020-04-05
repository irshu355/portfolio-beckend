from django.dispatch import receiver
from django.contrib.auth.models import User
from djoser.signals import user_registered
from ticker.models import UserProfile
from ticker.serializers import UserProfileSerializer
from ticker.utils.utils import UserTier
# do what you need here


@receiver(user_registered)
def printfunction(sender, **kwargs):
    user = kwargs["user"]
    obj = User.objects.get(username=user.username)
    profile = UserProfile.objects.create(
        user_id=obj.id, tier=UserTier.NORMAL.value)
    print("new user registered, user profile created")
