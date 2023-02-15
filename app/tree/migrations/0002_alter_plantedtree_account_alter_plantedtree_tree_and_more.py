# Generated by Django 4.0.9 on 2023-02-15 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0004_alter_account_members'),
        ('tree', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantedtree',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_trees', to='account.account'),
        ),
        migrations.AlterField(
            model_name='plantedtree',
            name='tree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='planted_trees', to='tree.tree'),
        ),
        migrations.AlterField(
            model_name='plantedtree',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_trees', to=settings.AUTH_USER_MODEL),
        ),
    ]
