# Generated by Django 2.1.7 on 2019-02-27 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('continuum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='suma',
            field=models.IntegerField(),
        ),
    ]