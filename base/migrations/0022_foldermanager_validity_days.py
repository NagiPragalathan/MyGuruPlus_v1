# Generated by Django 4.1.9 on 2024-01-27 04:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0021_rename_is_premium_usersubscription_course_premium"),
    ]

    operations = [
        migrations.AddField(
            model_name="foldermanager",
            name="validity_days",
            field=models.IntegerField(default=30),
        ),
    ]
