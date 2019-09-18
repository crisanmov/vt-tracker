from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from time import timezone
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    #Create User with email y password
	def _create_user(self, email, password, is_staff, is_superuser, **extra_fileds):
		now = timezone.now()

		if not email:
			raise ValueError('Debes introducir email')

		email = self.normalize_email(email)
		user = self.model(email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self,email, password=None, **extra_fields):
		return self._create_user(email, password, False, False, **extra_fields)

	def create_superuser(self,email, password=None, **extra_fields):
		return self._create_user(email, password, False, False, **extra_fields)

class User(AbstractBaseUser):

	email = models.EmailField(max_length=35, unique=True)
	username = models.CharField(max_length=50, unique=True)
	name = models.CharField(max_length=25, blank=True)
	lastP = models.CharField(max_length=20, blank=True)
	lastM = models.CharField(max_length=20, blank=True)
	address = models.CharField(max_length=60, blank=True)
	phone = models.CharField(max_length=10, blank=True)

	password = models.CharField(max_length=128, blank=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active= models.BooleanField(default=False)
	date_joined = models.DateTimeField(max_length=6, blank = True)
	#date_born = models.DateTimeField(max_length=6, blank = True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'name', 'lastP', 'lastM', 'address', 'phone']

	objects = CustomUserManager()

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
		db_table = ('user')
