# Generated by Django 2.1.1 on 2018-09-17 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='executeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostip', models.GenericIPAddressField(protocol='ipv4')),
                ('hostuser', models.CharField(max_length=32)),
                ('hostpass', models.CharField(blank=True, max_length=64, null=True)),
                ('hostcmd', models.CharField(blank=True, max_length=254, null=True)),
                ('excuteuser', models.CharField(max_length=32)),
                ('excuteip', models.GenericIPAddressField(blank=True, null=True, protocol='ipv4')),
                ('filepath', models.CharField(blank=True, max_length=128, null=True)),
                ('executetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
