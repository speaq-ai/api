from rest_framework.serializers import ModelSerializer
from users.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "assistant_session"]
