# Generated by Django 4.1.2 on 2022-10-31 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.UUIDField(null=True)),
                ('user_attr', models.CharField(max_length=255)),
                ('create_attr', models.CharField(max_length=255)),
                ('admin_attr', models.CharField(default='default value', max_length=255)),
            ],
        ),
    ]
