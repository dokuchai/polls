# Generated by Django 2.2.10 on 2021-02-02 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_useranswer_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='content.Answer', verbose_name='Ответ'),
        ),
    ]
