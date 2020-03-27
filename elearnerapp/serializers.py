from rest_framework import serializers
from elearnerapp.models import User

#User serializer

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields='__all__'
		