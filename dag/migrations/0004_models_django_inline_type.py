# Generated by Django 2.2.19 on 2021-03-08 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dag', '0003_businessrules_businessrulescode'),
    ]

    operations = [
        migrations.AddField(
            model_name='models',
            name='django_inline_type',
            field=models.CharField(blank=True, choices=[('TabularInline', 'TabularInline'), ('StackedInline', 'StackedInline')], max_length=30, null=True),
        ),
    ]
