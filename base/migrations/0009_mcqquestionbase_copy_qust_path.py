# Generated by Django 4.1.9 on 2024-01-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0008_mcqquestionbase_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="mcqquestionbase",
            name="copy_qust_path",
            field=models.TextField(default="root"),
            preserve_default=False,
        ),
    ]
