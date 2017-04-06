# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0002_blogcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='abstract',
            field=models.TextField(default=b'abstract', verbose_name=b'\xe6\x91\x98\xe8\xa6\x81'),
        ),
    ]
