# Generated by Django 4.1.3 on 2022-11-06 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0003_rename_phrase_phrase_ar_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='phrase',
            name='ar_text_no_harakat',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
