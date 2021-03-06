# Generated by Django 3.2.5 on 2022-06-06 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TradeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(db_index=True)),
                ('trade_id', models.CharField(max_length=64)),
                ('trade_seq', models.CharField(max_length=64)),
                ('timestamp', models.IntegerField(db_index=True)),
                ('currency', models.CharField(db_index=True, max_length=8)),
                ('instrument_name', models.CharField(db_index=True, max_length=64)),
                ('price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('direction', models.IntegerField()),
                ('index_price', models.FloatField()),
            ],
            options={
                'verbose_name': 'Trade Data',
                'verbose_name_plural': 'Trades Data',
            },
        ),
    ]
