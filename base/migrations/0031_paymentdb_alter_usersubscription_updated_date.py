# Generated by Django 4.1.9 on 2024-02-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0030_remove_usersubscription_validity_days_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentDb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("razorpay_order_id", models.CharField(max_length=255)),
                ("razorpay_payment_id", models.CharField(max_length=255)),
                ("razorpay_signature", models.CharField(max_length=255)),
                ("updated_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name="usersubscription",
            name="updated_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
