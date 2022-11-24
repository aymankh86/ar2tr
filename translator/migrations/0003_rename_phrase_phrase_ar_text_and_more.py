# Generated by Django 4.1.3 on 2022-11-05 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0002_phrase_phrase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phrase',
            old_name='phrase',
            new_name='ar_text',
        ),
        migrations.RenameField(
            model_name='phrase',
            old_name='translation',
            new_name='tr_text',
        ),
        migrations.RemoveField(
            model_name='phrase',
            name='from_language',
        ),
        migrations.RemoveField(
            model_name='phrase',
            name='to_language',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]
