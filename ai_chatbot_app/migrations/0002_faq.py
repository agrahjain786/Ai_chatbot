# Generated by Django 4.2.11 on 2024-04-15 07:19
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_chatbot_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
        ),
    ]
