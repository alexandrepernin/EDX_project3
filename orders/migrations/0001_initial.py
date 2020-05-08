# Generated by Django 2.0.3 on 2020-05-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('toppings', models.IntegerField()),
                ('size', models.CharField(max_length=64)),
            ],
        ),
    ]
