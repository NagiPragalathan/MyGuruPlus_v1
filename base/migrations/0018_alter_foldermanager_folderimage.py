# Generated by Django 4.1.9 on 2024-01-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0017_alter_foldermanager_folderimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="foldermanager",
            name="FolderImage",
            field=models.FileField(upload_to="Folder_profile_img/"),
        ),
    ]
