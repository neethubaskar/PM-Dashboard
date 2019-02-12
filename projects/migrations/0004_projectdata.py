# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-12 11:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_delete_gitlabdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_opend_issues', models.IntegerField(blank=True, null=True)),
                ('int_commits', models.IntegerField(blank=True, null=True)),
                ('int_doing_issues', models.IntegerField(blank=True, null=True)),
                ('dat_fetching', models.DateTimeField()),
                ('fk_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]