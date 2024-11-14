# Generated by Django 5.1rc1 on 2024-11-01 19:11

from django.db import migrations


class Migration(migrations.Migration):

    def populate_db(apps, schema_editor):
        SecurityOptions = apps.get_model("web_server", "SecurityOptions")
        option1 = SecurityOptions(option_code="ECDHE-ECDSA-AES256-GCM-SHA384",
                                  option_description="Best for Security",
                                  option_text="This encryption suite offers a high level of security, making it suitable "
                                              "for scenarios where protecting sensitive information is critical.<br>"
                                              "It provides strong encryption that is more resistant to attacks, "
                                              "making it ideal for applications or devices where security is prioritized over performance.<br>"
                                              "This choice is perfect for environments handling sensitive or confidential data that needs maximum protection.",
                                  is_selected=True)
        option1.save()
        option2 = SecurityOptions(option_code="ECDHE-ECDSA-AES128-GCM-SHA256",
                                  option_description="Best for Performance",
                                  option_text="This suite balances security with performance, offering adequate protection "
                                              "while requiring fewer resources to operate efficiently.<br>"
                                              "It’s designed for devices that may have limited processing power or memory, "
                                              "such as smaller IoT devices or systems where speed is important.<br>"
                                              "This option provides good security without overburdening resource-limited devices,"
                                              " making it ideal for applications where performance is critical.",
                                  is_selected=False)
        option2.save()
        option3 = SecurityOptions(option_code="ECDHE-ECDSA-CHACHA20-POLY1305",
                                  option_description="Best for Mobile Devices",
                                  option_text="This suite is particularly suited for mobile devices that lack specialized hardware to speed up encryption.<br>"
                                              "The ChaCha20 encryption algorithm in this suite is designed to perform efficiently even on devices without"
                                              " encryption hardware, making it perfect for mobile phones, tablets, or other devices where battery life and"
                                              " processing power are limited.<br>"
                                              "<br>This option helps ensure secure connections without significantly impacting device performance or battery life.",
                                  is_selected=False)
        option3.save()

    dependencies = [
        ('web_server', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db),
    ]
