# Generated by Django 4.0.3 on 2022-05-08 07:26

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
            name='AbstractFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('type', models.CharField(choices=[('Model', 'Model'), ('Image', 'Image'), ('MP3', 'Mp3'), ('Other', 'Other')], default='Other', max_length=5)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('abstractfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.abstractfile')),
                ('object', models.FileField(blank=True, null=True, upload_to='models')),
                ('description', models.TextField(blank=True, null=True)),
                ('parameters', models.JSONField(default={})),
            ],
            options={
                'verbose_name_plural': 'Models',
            },
            bases=('app.abstractfile',),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('abstractfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.abstractfile')),
                ('is_original', models.BooleanField(default=False)),
                ('object', models.ImageField(blank=True, null=True, upload_to='files')),
                ('original', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.file')),
                ('selected_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.model')),
            ],
            options={
                'verbose_name_plural': 'Files',
            },
            bases=('app.abstractfile',),
        ),
    ]