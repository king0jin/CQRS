# Generated by Django 5.1.1 on 2024-11-20 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('bid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('pages', models.IntegerField()),
                ('price', models.IntegerField()),
                ('published_date', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
    ]
