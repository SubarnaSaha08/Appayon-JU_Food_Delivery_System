# Generated by Django 3.1.2 on 2024-05-31 19:29

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
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=50, verbose_name='Employee ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(max_length=14, verbose_name='Mobile')),
                ('email', models.EmailField(max_length=254)),
                ('image', models.ImageField(default='media/default_user.png', upload_to='customer_pics', verbose_name='Profile Picture')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('address', models.TextField(default='', max_length=1000)),
                ('area', models.CharField(choices=[('1', 'সাভার'), ('2', 'প্রান্তিক গেইট '), ('3', 'সকল মহিলা হল'), ('4', 'ডেইরি গেইট'), ('5', 'সামাজিক বিজ্ঞান অনুষদ, গণিত ও পরিসংখ্যান বিভাগ, নতুন কলা ভবন, পদার্থবিজ্ঞান বিভাগ, রসায়ন বিভাগ'), ('6', 'পুরাতন কলা ভবন, ব্যবসায় শিক্ষা অনুষদ, আল বেরুনি হল'), ('7', 'ভূতত্ত্ব, সি.এস.ই ও পরিবেশ বিজ্ঞান ভবন, বটতলা, বঙ্গবন্ধু হল, আ.ফ.ম  কামালউদ্দিন হল, সালাম বরকত হল'), ('8', 'মওলানা ভাসানী হল, বিশ্বকবি রবীন্দ্রনাথ ঠাকুর হল, রফিক জব্বার হল'), ('9', 'জীববিজ্ঞান অনুষদ'), ('10', 'মীর মশাররফ হোসেন হল')], max_length=50)),
                ('phone', models.CharField(max_length=14, verbose_name='Mobile')),
                ('email', models.EmailField(max_length=254)),
                ('image', models.ImageField(default='media/default_user.png', upload_to='customer_pics', verbose_name='Profile Picture')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
