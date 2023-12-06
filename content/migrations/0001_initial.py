# Generated by Django 4.2.7 on 2023-11-28 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('type', models.CharField(choices=[('premium', 'Premium'), ('free', 'Free')], max_length=7, verbose_name='type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('views', models.IntegerField(default=0, verbose_name='views')),
                ('is_published', models.BooleanField(default=False, verbose_name='published')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'content',
                'verbose_name_plural': 'contents',
            },
        ),
    ]
