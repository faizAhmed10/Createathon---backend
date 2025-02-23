# Generated by Django 5.1.6 on 2025-02-22 12:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_category_challenge_test_cases_and_more'),
        ('progress', '0002_discussion_comment_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.challenge'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
