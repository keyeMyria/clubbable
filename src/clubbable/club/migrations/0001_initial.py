from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('galleries', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, editable=False, primary_key=True)),
                ('date_of_listing', models.DateField()),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('initials', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('admitted_to_club', models.BooleanField(default=False)),
                ('date_admitted', models.DateField(blank=True, null=True)),
                ('delisted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, editable=False, primary_key=True)),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('name', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('number_of_tables', models.PositiveSmallIntegerField()),
                ('comment', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('initials', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('post_title', models.CharField(blank=True, max_length=100)),
                ('familiar_name', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=150)),
                ('send_emails', models.BooleanField(default=False)),
                ('qualification_art', models.BooleanField(default=False)),
                ('qualification_drama', models.BooleanField(default=False)),
                ('qualification_literature', models.BooleanField(default=False)),
                ('qualification_music', models.BooleanField(default=False)),
                ('qualification_science', models.BooleanField(default=False)),
                ('hon_life_member', models.BooleanField(verbose_name='Honorary life member', default=False)),
                ('canonisation_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_image', models.ForeignKey('galleries.Image', models.SET_NULL, null=True, blank=True)),
            ],
            options={
                'ordering': ('last_name', 'familiar_name'),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('member', models.OneToOneField('club.Member', models.SET_NULL, null=True, blank=True)),
                ('user', models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='guest',
            name='member',
            field=models.ForeignKey('club.Member', models.SET_NULL, null=True, blank=True),
        ),
    ]
