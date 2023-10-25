from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager, BaseUserManager, PermissionsMixin

# Create your models here.
class UseService(models.Model):
    user = models.OneToOneField('UserInfo', models.DO_NOTHING, primary_key=False)
    service_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=30, blank=True, null=True)
    job_name = models.CharField(max_length=255, blank=True, null=True)
    use_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'use_service'


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_id, gender, birth_date, password=None):
        if not user_id:
            raise ValueError("Users must have an email address")
        user = self.model(
            user_id=self.normalize_email(user_id),
            gender=gender,
            birth_date=birth_date,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, user_id, password, gender, birth_date):
        user = self.create_user(
            user_id,
            password=password,
            gender=gender,
            birth_date=birth_date,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user
        
class UserInfo(AbstractBaseUser, PermissionsMixin):
    user_id = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(max_length=5, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=20, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'user_info'
    
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['gender', 'birth_date', 'address']

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
