# Generated by Django 2.2.5 on 2020-09-20 23:08

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
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('images', models.ImageField(upload_to='')),
                ('date', models.DateTimeField()),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=50)),
                ('max_capacity', models.IntegerField()),
                ('slug', models.SlugField(blank=True, null=True)),
                ('attendees', models.ManyToManyField(related_name='EventsAttending', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MyEvents', related_query_name='organizer', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='events', to='events.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('following_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('user_id', 'following_user_id')},
            },
        ),
    ]