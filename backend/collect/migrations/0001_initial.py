# Generated by Django 5.0.4 on 2024-05-06 09:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='donations/images/')),
                ('goal', models.CharField(choices=[('Wedding', 'Свадьба'), ('PC Upgrade', 'Апгрейд ПК'), ('Treatment', 'На лечение'), ('For a dream life', 'На красивую жизнь'), ('Birthday', 'День рождения'), ('Animal Shelter', 'Приют для животных')], max_length=200)),
                ('goal_amount', models.PositiveIntegerField(blank=True, default=None)),
                ('description', models.TextField()),
                ('due_to', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collect', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Групповой денежный сбор',
                'verbose_name_plural': 'Групповые денежные сборы',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('comment', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('donation_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='collect.collect')),
                ('donator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Платёж (донация)',
                'verbose_name_plural': 'Платежи (донации)',
                'ordering': ('date',),
            },
        ),
    ]
