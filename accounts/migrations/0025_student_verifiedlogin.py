# Generated by Django 4.2 on 2023-06-04 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_alter_student_approvedaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='verifiedLogin',
            field=models.BooleanField(blank=True, default=False, max_length=100, null=True),
        ),
    ]
