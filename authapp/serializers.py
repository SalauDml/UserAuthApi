from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password','email']
        extra_kwargs = {"first_name":{'required': True},
                        "last_name":{'required': True},
                        "email":{'required': True} }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

