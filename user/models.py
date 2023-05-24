from django.db import models
from django.contrib.auth.models import User


AUTH_PROVIDERS = {'google': 'google','email': 'email'}

class UserData(models.Model):
  id = models.BigAutoField(primary_key=True)
  # username = models.CharField(max_length=16,unique=True,null=True)
  # email = models.CharField(max_length=50, unique=True)
  # password = models.CharField(max_length=35)
  # is_active=models.BooleanField(default=False)

  


  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

  class Meta:
      db_table='User'

  def _str_(self):
      return self.user.username

  
  