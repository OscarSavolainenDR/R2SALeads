from rest_framework import serializers
from ..models import User, Session#, ResetPassword

class SignInSerializer(serializers.ModelSerializer):

    # Redefine this so isunique constraint doesn't need to be met, 
    # otherwise returning validusername code would be rejected by serializer
    username = serializers.CharField(validators=[])

    class Meta:
        model = User
        fields = ('username', 'password')
 
class SignOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()
 

class SignUpSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(validators=[])
    # email = serializers.CharField(validators=[])
    # password = serializers.CharField(validators=[])
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('key')

# class ForgotPasswordSerializer(serializers.ModelSerializer):
#     # key = serializers.CharField()
#     class Meta:
#         model = ResetPassword
#         fields = ('key')