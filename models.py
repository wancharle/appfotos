# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from paginas.models import Unidade
from image_cropping import ImageRatioField
from paginas.util import get_unidade__identificador

class Categoria(models.Model):
    nome = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s" % self.nome


class EventoManager(models.Manager):
    def da_unidade(self,request):
        unidade = get_unidade__identificador(request)
        return self.filter(Q(unidade__isnull=True) | Q(unidade__identificador=unidade)).order_by("-data",'-unidade')


class Evento(models.Model): 
    unidade = models.ForeignKey(Unidade,blank=True,null=True)
    titulo = models.CharField(max_length=50)
    resumo = models.CharField(max_length=100)
    descricao = models.TextField()

    categoria = models.ForeignKey(Categoria,null=True,blank=True)
    
    data = models.DateTimeField(verbose_name="data")
    foto_principal = models.ImageField(upload_to="eventos/", help_text=u"imagem principal do evento. Exemplo de proporção: 170x X 100px")
    cropping = ImageRatioField('foto_principal', '170x100')

    objects = EventoManager()
    def __unicode__(self):
        return u"%s" % self.titulo

    def get_fotos(self):
        return self.foto_set.all()
    
class Foto(models.Model):
    evento = models.ForeignKey(Evento)
    legenda = models.CharField(max_length=150,null=True, blank=True)
    foto = models.ImageField(upload_to="eventos/%Y/%m/%d/" )
    cropping = ImageRatioField('foto', '800x600')

    def __unicode__(self):
        return u"%s - %s" % (self.evento.titulo, self.legenda)
