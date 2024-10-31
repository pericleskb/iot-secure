from django.db import models

class User(models.Model):
        username = models.CharField(max_length=100)
        password = models.CharField(max_length=256)
        
        def __str__(self):
                return self.username + ":" + self.password


class SecurityOptions(models.Model):
        option_code = models.CharField(max_length=100)
        option_description = models.CharField(max_length=100)
        option_text = models.CharField(max_length=2000)

        def __str__(self):
                return self.option_code + ":" + self.option_description