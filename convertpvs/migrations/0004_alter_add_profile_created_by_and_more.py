# Generated by Django 4.2.1 on 2023-06-19 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convertpvs', '0003_alter_add_profile_options_alter_audit_log_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_profile',
            name='created_by',
            field=models.CharField(auto_created=True, default='admin', editable=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='add_profile',
            name='updated_by',
            field=models.CharField(auto_created=True, default='admin', editable=False, max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),

    ]