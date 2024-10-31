from django.db import models

class User(models.Model):
        username = models.CharField(max_length=100)
        password = models.CharField(max_length=256)
        
        def __str__(self):
                return f"self.username:self.password"


class SecurityOptions(models.Model):
        option_code = models.CharField(max_length=100)
        option_description = models.CharField(max_length=100)
        option_text = models.CharField(max_length=2000)
        isSelected = models.BooleanField(False)

        def __str__(self):
                return f"self.option_code:self.option_description"

class SelectedOption(models.Model):
    option = models.OneToOneField(
        SecurityOptions,
        on_delete=models.CASCADE,
        primary_key=True,  # Ensures only one row in this table
    )

    def __str__(self):
        return f"Selected Option: {self.option.name}"