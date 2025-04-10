# Generated by Django 3.2.7 on 2024-06-04 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estabelecimentos', '0004_auto_20240513_0840'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profissionais', '0001_initial'),
        ('relatorios', '0005_auto_20240215_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade de vagas')),
                ('tipoConsulta', models.IntegerField(choices=[(1, 'Consulta'), (2, 'Retorno')], verbose_name='Tipo de consulta')),
                ('dataAgendamento', models.DateField(verbose_name='Data de agendamento')),
                ('horarioAgendamento', models.DateTimeField(verbose_name='Horário de agendamento')),
                ('updatedBy_user', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('createdBy_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='estabelecimentos.estabelecimento')),
                ('procedimento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='relatorios.dicionariodeprocedimentos')),
                ('profissional', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='profissionais.profissional')),
            ],
        ),
    ]
