# Generated by Django 3.1.2 on 2024-06-01 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='area',
            field=models.CharField(choices=[('1', 'সাভার'), ('2', 'প্রান্তিক গেইট '), ('3', 'সকল মহিলা হল'), ('4', 'ডেইরি গেইট'), ('5', 'সামাজিক বিজ্ঞান অনুষদ, গণিত ও পরিসংখ্যান বিভাগ, নতুন কলা ভবন, পদার্থবিজ্ঞান বিভাগ, রসায়ন বিভাগ'), ('6', 'পুরাতন কলা ভবন, ব্যবসায় শিক্ষা অনুষদ, আল বেরুনি হল'), ('7', 'ভূতত্ত্ব, সি.এস.ই ও পরিবেশ বিজ্ঞান ভবন, বটতলা, বঙ্গবন্ধু হল, আ.ফ.ম  কামালউদ্দিন হল, সালাম বরকত হল'), ('8', 'মওলানা ভাসানী হল, বিশ্বকবি রবীন্দ্রনাথ ঠাকুর হল, রফিক জব্বার হল'), ('9', 'জীববিজ্ঞান অনুষদ'), ('10', 'মীর মশাররফ হোসেন হল'), ('11', 'বিশমাইল')], max_length=50),
        ),
    ]
