# Generated by Django 4.1.3 on 2022-11-18 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0004_phrase_ar_text_no_harakat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('tr_text', models.CharField(max_length=255)),
                ('ar_text', models.CharField(max_length=255)),
                ('job_type', models.CharField(max_length=50)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggestion_category', to='translator.category')),
                ('phrase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestion_phrase', to='translator.phrase')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
