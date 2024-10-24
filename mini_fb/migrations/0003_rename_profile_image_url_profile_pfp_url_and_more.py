# Generated by Django 5.1.1 on 2024-10-15 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0002_statusmessage"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="profile_image_url",
            new_name="pfp_url",
        ),
        migrations.AlterField(
            model_name="statusmessage",
            name="message",
            field=models.CharField(max_length=500),
        ),
    ]