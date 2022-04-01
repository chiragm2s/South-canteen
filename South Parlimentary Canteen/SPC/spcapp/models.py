from inspect import signature
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,)
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# User = get_user_model()



# Create your models here.

class User(AbstractUser):
    #id = models.AutoField(primary_key=True)
    username    = None
    name        = models.CharField(max_length=20 )
    email       = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    is_verified = models.IntegerField(default=0)
    is_admin   = models.BooleanField('is_admin',default=False)
    is_customer = models.BooleanField('Is customer',default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # address     = models.CharField(max_length=2500,default="")
    # state        = models.CharField(max_length=250,default="")
    # place        = models.CharField(max_length=250,default="")
    # pincode      = models.IntegerField(default=False)

    def __str__(self):
        return self.email

#for image upload
def upload_to(instance,filename):
    # return 'posts/{filename}'.format(filename=filename)
    return '/'.join(['images',str(instance.image),str(instance.signature),filename.format(filename=filename)])


class userDetails(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id=models.ForeignKey('User', on_delete=models.CASCADE)
    firstname        = models.CharField(max_length=20 )
    lastname        = models.CharField(max_length=20 )
    image=models.ImageField(_("IMAGE"),upload_to=upload_to)
    parlimantary       = models.IntegerField(default=False)
    sategovt       = models.IntegerField(default=False)
    centralgovt       = models.IntegerField(default=False)
    exmenwidow       = models.IntegerField(default=False)
    others       = models.IntegerField(default=False)
    service       = models.IntegerField(default=False)
    retired       = models.IntegerField(default=False)
    rank = models.CharField(max_length=255)
    forceno = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)#, related_name='place of work'
    force = models.CharField(max_length=255)#, related_name='Department Name'
    nameofspouse = models.CharField(max_length=255)#, related_name='place of work'
    address = models.CharField(max_length=255)
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    dob = models.DateField(max_length=8)
    pin = models.CharField(max_length=6)
    signature = models.ImageField(_("IMAGE"),upload_to=upload_to)

    
    def __str__(self):
        return self.UserDetails