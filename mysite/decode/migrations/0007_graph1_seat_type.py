# Generated by Django 5.0.6 on 2024-06-11 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decode', '0006_remove_graph1_seat_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph1',
            name='seat_type',
            field=models.CharField(default='OPEN', max_length=50),
        ),
    ]
