# Generated by Django 3.1.3 on 2021-04-06 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20210405_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.postcomment'),
        ),
    ]
