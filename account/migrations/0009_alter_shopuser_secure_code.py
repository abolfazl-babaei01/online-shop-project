# Generated by Django 5.0.6 on 2024-09-03 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_shopuser_secure_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='secure_code',
            field=models.CharField(default='4WW58JdP3lPTR1Ov8bomzSTfIEI7zSIrlsxOAwOV3Otq9C6uKyi7lArvTovpnoSPqqSIxEu2Z', max_length=73, verbose_name='کد امنبتی '),
        ),
    ]
