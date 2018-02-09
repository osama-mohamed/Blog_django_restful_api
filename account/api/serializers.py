from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
    )

from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class RegisterSerializer(ModelSerializer):
    first_name = CharField(label='First name')
    last_name = CharField(label='Last name')
    username = CharField(label='Username')
    email = EmailField(label='E-mail')
    email_confirmation = EmailField(label='Confirm E-mail')
    password = CharField(label='Password')
    password_confirmation = CharField(label='Confirm Password')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'email_confirmation',
            'password',
            'password_confirmation',
        ]
        extra_kwargs = {'password':
                            {'write_only': True}
                        }

    def validate_username(self, username):
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise ValidationError('This username is already registered before!')
        return username

    def validate_email_confirmation(self, email_confirmation):
        data = self.get_initial()
        email = data.get('email')
        email_confirmation = email_confirmation
        if email != email_confirmation:
            raise ValidationError('Email dose not matched!')
        qs = User.objects.filter(email__iexact=email_confirmation)
        if qs.exists():
            raise ValidationError('This email is already registered before!')
        return email_confirmation

    def validate_password_confirmation(self, password_confirmation):
        data = self.get_initial()
        password = data.get('password')
        password_confirmation = password_confirmation
        if password != password_confirmation:
            raise ValidationError('Passwords dose not matched!')
        return password_confirmation

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return validated_data


class LoginSerializer(ModelSerializer):
    username = CharField(label='Username', required=False, allow_blank=True)
    email = EmailField(label='E-mail', required=False, allow_blank=True)
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password')
        if not username and not email:
            raise ValidationError('Username or email are required for login!')
        user = User.objects.filter(
            Q(username=username, is_active=True) |
            Q(email=email, is_active=True)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_data = user.first()
        else:
            raise ValidationError('Username or Email is not valid!')
        if user_data:
            if not user_data.check_password(password):
                raise ValidationError('Incorrect Password!')
        data['token'] = 'random token is here for test'
        return data
