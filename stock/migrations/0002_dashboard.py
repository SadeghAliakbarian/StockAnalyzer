# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-04 03:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Company')),
                ('second_company', models.ManyToManyField(related_name='dashboard_requests_created', to='stock.Company')),
            ],
        ),
    ]
