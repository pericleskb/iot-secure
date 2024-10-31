# web_server/db_manage/populate_db.py
from django.core.management.base import BaseCommand
from web_server_project.web_server.models import SecurityOptions

class Command(BaseCommand):
	help = 'Populate with supported Security Options'
	
	def handle(self, *args, **kwargs):
		self.stdout.write("Running")
		if not SecurityOptions.objects.exists():
			#Add initial data
			SecurityOptions.objects.bulk_create([
				SecurityOptions(option_code="ECDHE-ECDSA-AES256-GCM-SHA384", option_description="Best for Security", option_text="This is an option used for blah blah<br><br>Also blah blah"),
				SecurityOptions(option_code="ECDHE-ECDSA-AES128-GCM-SHA256", option_description="Best for Performance", option_text="This is an option used for blah blah<br><br>Also blah blah"),
				SecurityOptions(option_code="ECDHE-ECDSA-CHACHA20-POLY1305", option_description="Best for Mobile Devices", option_text="This is an option used for blah blah<br><br>Also blah blah"),  
			])
			self.stdout.write(self.style.SUCCESS("Initial data added to DB"))
		else:
			self.stdout.write("DB already populated")
