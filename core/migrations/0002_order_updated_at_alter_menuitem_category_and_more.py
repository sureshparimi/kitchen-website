# Generated by Django 5.1.6 on 2025-03-02 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="menu_items",
                to="core.category",
            ),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="menu_items/"),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="preparation_time",
            field=models.PositiveIntegerField(help_text="Preparation time in minutes"),
        ),
    ]
