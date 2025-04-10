from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import re
# Create your models here.

class Perfil(models.Model):
    celular = models.CharField(max_length = 15, null=True)
    cpf = models.CharField(max_length=14, null=True)
    cargo = models.CharField(max_length=50, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_or_update_user_profile(instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
    # instance.profile.save()


# Create your models here.

class Profile(models.Model):
    cns = models.CharField(null=True, blank=True, max_length=19, unique=True, verbose_name="Cartao Sus")
    cpf = models.CharField(null=True, blank=True, max_length=11, unique=True, verbose_name="CPF")
    nome = models.CharField(null=True, blank=True, max_length=255, verbose_name="Nome")
    sexo = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Sexo")
    dataNascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    cargo = models.CharField(null=True, blank=True, max_length=255)
    altura = models.CharField(default='0', max_length=4, verbose_name="Altura")
    peso = models.CharField(default='0', max_length=6, verbose_name="Peso")
    nomeDaMae = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nome da Mãe")
    nomeDoPai = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nome do Pai")
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    telefone1 = models.CharField(null=True, blank=True, max_length=16, verbose_name="Telefone/Celular")
    telefone2 = models.CharField(max_length=16, null=True, blank=True, verbose_name="Telefone para Recado")
    celular1 = models.CharField(max_length=16, null=True, blank=True, verbose_name="Celular para Contato")
    celular2 = models.CharField(max_length=16, null=True, blank=True, verbose_name="Celular para Recado")
    allowMessage = models.BooleanField(default=False, blank=False, verbose_name="Aceita receber mensagem? (Ex: Whatsapp, Telegram, sms...)") #atender a LGPD
    isVisible = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        self.cns = re.sub(r'[^\w\s]','',self.cns)
        self.telefone1 = re.sub(r'[^\w\s]','',self.telefone1)
        # self.telefone2 = re.sub(r'[^\w\s]','',self.telefone2)
        self.celular1 = re.sub(r'[^\w\s]','',self.celular1)
        # self.celular2 = re.sub(r'[^\w\s]','',self.celular2)
        super(Profile,self).save(*args,**kwargs)

class Contacts(models.Model):
    STATUS_CHOICES = [
        (1,'Telefone'),
        (2,'Celular'),
        (3,'E-mail'),
        (4,'Facebook'),
        (5,'IG'),
        (6,'Linkedin'),
        (7,'Whatsapp'),        
    ]

    tipo = models.IntegerField(choices=STATUS_CHOICES, default=1)
    contato = models.CharField(max_length=100, verbose_name="Contato")    
    allowMessage = models.BooleanField(default=False, blank=False, verbose_name="Aceita receber mensagem nesse contato?") #atender a LGPD
    isVisible = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
