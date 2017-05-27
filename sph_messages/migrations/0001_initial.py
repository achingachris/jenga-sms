# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-27 07:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.Contact_Group')),
            ],
            options={
                'db_table': 'sph_messages',
            },
        ),
        migrations.CreateModel(
            name='SmsSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('api_key', models.CharField(max_length=256)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sph_settings',
            },
        ),
    ]
