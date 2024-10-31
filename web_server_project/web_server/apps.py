from django.apps import AppConfig
from django.db.utils import OperationalError
from django.db import ProgrammingError

class WebServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_server'


class MyAppConfig(AppConfig):

    def ready(self):
        from models import SecurityOptions
        try:
            # Check if the table is empty
            if not SecurityOptions.objects.exists():
                # Add initial data
                SecurityOptions.objects.bulk_create([
                    SecurityOptions(option_code="ECDHE-ECDSA-AES256-GCM-SHA384", option_description="Best for Security", option_text="This is an option used for blah blah<br><br>Also blah blah"),
                    SecurityOptions(option_code="ECDHE-ECDSA-AES128-GCM-SHA256", option_description="Best for Performance", option_text="This is an option used for blah blah<br><br>Also blah blah"),
                    SecurityOptions(option_code="ECDHE-ECDSA-CHACHA20-POLY1305", option_description="Best for Mobile Devices", option_text="This is an option used for blah blah<br><br>Also blah blah"),
                    # Add more as needed
                ])
                print("Initial data added to MyModel.")
        except (OperationalError, ProgrammingError):
            # This can occur if the database or table isn't created yet.
            pass