from django.db import models
from eventex.core.managers import KindContactManager, KindQuerySet #,EmailContactManager, PhoneContactManager
from eventex.subscriptions.validators import validate_cpf
from django.shortcuts import resolve_url as r

# class SpeakerOld(models.Model):
#     name = 'Grace Hopper'
#     website = 'https://hbn.link/hopper-site'
#     photo = 'https://hbn.link/hopper-pic'
#     title = 'Programadora e almirante'
#     description ='Inventora do compilador, criadora da linguagem de programação Flow-Matic. A Linguagem serviu de base para a linguagem COBOL permitindo a popularização das aplicações comerciais.'

class Speaker(models.Model):
    name = models.CharField('nome',max_length=255)
    title = models.CharField('título',max_length=100)
    slug = models.SlugField('slug')
    photo = models.URLField('foto')
    website = models.URLField('website', blank=True)
    description = models.TextField('descrição', blank=True)
    #created_at = models.DateTimeField('criado em',auto_now=True)

    class Meta:
        verbose_name_plural = 'palestrantes'
        verbose_name = 'palestrante'
        #ordering = ('-created_at',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('speaker_detail', slug=self.slug)

class Contact(models.Model):
    EMAIL = 'E'
    PHONE = 'P'

    KINDS=(
        (EMAIL,'Email'),
        (PHONE,'Telefone'),
    )
    
    speaker = models.ForeignKey('Speaker', on_delete=models.CASCADE, verbose_name='palestrante')
    kind = models.CharField('tipo', max_length=1, choices=KINDS)
    value = models.CharField('valor', max_length=255)

    #objects = models.Manager()
    # emails = EmailContactManager()
    # phones = PhoneContactManager()
    #objects = KindContactManager()
    objects = KindQuerySet.as_manager()
    class Meta:
        verbose_name_plural = 'contatos'
        verbose_name = 'contato'
    
    def __str__(self):
        return self.value  

class Talk(models.Model):
    title = models.CharField('título', max_length=100)
    start = models.TimeField('início', blank=True, null=True)
    description = models.TextField('descrição', blank=True)
    speakers = models.ManyToManyField("Speaker", verbose_name='palestrantes', blank=True)

    class Meta:
        verbose_name_plural = 'palestras'
        verbose_name = 'palestra'
    
    def __str__(self):
        return self.title  