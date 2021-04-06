# Generated by Django 3.1.7 on 2021-04-03 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_auto_20210403_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.post'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='reply_at',
            field=models.ManyToManyField(blank=True, null=True, related_name='replie_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
