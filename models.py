# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from image_cropping import ImageRatioField

class Categoria(models.Model):
    nome = models.CharField(max_length=20)
    nome_en = models.CharField(max_length=20,verbose_name=u"nome em inglês")
    info = models.TextField(help_text=u'informações sobre as suites desse tipo')
    info_en = models.TextField(verbose_name=u"info em inglês",help_text=u'informações sobre as suites desse tipo')
    preco = models.DecimalField(max_digits=8, decimal_places=2,help_text=u'preços da diarias para as suites deste tipo')
    ordem = models.IntegerField(default=1,null=True,blank=True)
    
    class Meta:
        verbose_name = u"tipo de suíte"		
        verbose_name_plural = u"tipos de suítes"		
        ordering = ('ordem',)

    def __unicode__(self):
        return u"%s" % self.nome


class Evento(models.Model): 
    titulo = models.CharField(max_length=50)
    resumo = models.CharField(max_length=100,default=" ",null=True,blank=True)
    descricao = models.TextField()
    descricao_en = models.TextField(verbose_name=u"descrição em inglês")

    categoria = models.ForeignKey(Categoria,null=True,blank=False)
    
    data = models.DateTimeField(verbose_name="data",null=True,blank=True)
    foto_principal = models.ImageField(upload_to=u"eventos/", help_text=u"imagem principal. Exemplo de proporção: 757px X 563px")
    cropping = ImageRatioField(u'foto_principal', '757x563')
    ordem = models.IntegerField(default=1,null=True,blank=True)
    
    class Meta:
        verbose_name = u"suíte"

    def __unicode__(self):
        return u"%s" % self.titulo

    def get_fotos(self):
        return self.foto_set.all()
    
class Foto(models.Model):
    evento = models.ForeignKey(Evento)
    legenda = models.CharField(max_length=150,null=True, blank=True)
    foto = models.ImageField(upload_to=u"eventos/%Y/%m/%d/" )
    cropping = ImageRatioField('foto', '400x300',free_crop=True)

    def __unicode__(self):
        return u"%s - %s" % (self.evento.titulo, self.legenda)



# vim: set ts=4 sw=4 sts=4 expandtab:
