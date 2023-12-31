# Generated by Django 4.2.1 on 2023-10-27 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acesso', '0004_pessoa_nome_alter_endereco_pessoa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='pessoa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enderecos', to='acesso.pessoa'),
        ),
        migrations.AlterField(
            model_name='veiculo',
            name='pessoa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='veiculos', to='acesso.pessoa'),
        ),
    ]
