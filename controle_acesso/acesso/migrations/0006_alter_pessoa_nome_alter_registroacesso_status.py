# Generated by Django 4.2.1 on 2023-10-28 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acesso', '0005_alter_endereco_pessoa_alter_veiculo_pessoa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='registroacesso',
            name='status',
            field=models.CharField(choices=[('E', 'Em andamento'), ('F', 'Finalizado')], default='E', max_length=1),
        ),
    ]
