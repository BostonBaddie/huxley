# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-05 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [('core', '0026_auto_20171206_1716'), ]

    operations = [
        migrations.CreateModel(
            name='CommitteeFeedback',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('comment', models.TextField()),
                ('committee', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='core.Committee')),
            ],
            options={
                'db_table': 'committee_feedback',
            }, ),
        migrations.AddField(
            model_name='delegate',
            name='committee_feedback_submitted',
            field=models.BooleanField(default=False), ),
        migrations.AlterField(
            model_name='registration',
            name='committee_preferences',
            field=models.ManyToManyField(
                blank=True, null=True, to='core.Committee'), ),
    ]
