# Generated by Django 5.1.1 on 2024-11-13 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="voter",
            name="date_of_registration",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v20state",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v21primary",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v21town",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v22general",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v23town",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="voter_score",
            field=models.IntegerField(default=0),
        ),
    ]
