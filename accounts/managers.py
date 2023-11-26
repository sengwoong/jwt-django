from django.contrib.auth.base_user import BaseUserManager
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import DefaultAccountAdapter

class CustomRegisterSerializer(RegisterSerializer):

    def save(self, request):
        user = super().save(request)
        user.profile_image = self.data.get('profile_image')
        user.user_id = self.data.get('user_id')
        user.name = self.data.get('name')
        user.user_nick_name = self.data.get('user_nick_name')
        user.user_classification = self.data.get('user_classification')
        user.age = self.data.get('age')
        user.gender = self.data.get('gender')
        user.save()
        return user

class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, False)
        user.profile_image = request.data.get('profile_image')
        user.user_id = request.data.get('user_id')
        user.name = request.data.get('name')
        user.user_nick_name = request.data.get('user_nick_name')
        user.user_classification = request.data.get('user_classification')
        user.age = request.data.get('age')
        user.gender = request.data.get('gender')

        if commit:
            user.save()

        return user

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):


        print(email)
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser
