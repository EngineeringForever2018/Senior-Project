# Generated by Django 3.1.5 on 2021-04-20 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='api.classroom'),
        ),
    ]
