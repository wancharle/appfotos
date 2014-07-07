from django.contrib import admin
from django.http import HttpResponseRedirect
from appfotos.models import Evento, Foto, Categoria
from image_cropping import ImageCroppingMixin
from easy_thumbnails.files import get_thumbnailer
from tinymce.widgets import TinyMCE
from django import forms

class FotoInline(admin.TabularInline):
    model = Foto
    fields = ('foto','legenda')


class SuiteForm(forms.ModelForm):
    descricao = forms.CharField(widget=TinyMCE(attrs={"rows":20,"cols":100}))
    descricao_en = forms.CharField(widget=TinyMCE(attrs={"rows":20,"cols":100}))
   
    class Meta:
        model = Evento

class EventoAdmin(ImageCroppingMixin,admin.ModelAdmin):
    inlines = [FotoInline,] 
    actions = ['enviar_zip_de_fotos',]
    exclude = [ 'data','resumo']
    form = SuiteForm
    list_display = ['titulo', 'categoria', 'imagem','galeria','ordem']

    def imagem(self,obj):
        thumbnail_url = get_thumbnailer(obj.foto_principal).get_thumbnail({
            'size': (133, 100),
            'box': obj.cropping,
            'crop': True,
            'detail': True,
        }).url

        return u"<img src='%s'>" % thumbnail_url
    imagem.allow_tags=True
    imagem.short_description= "foto principal"

    def galeria(self,obj):
        gal = u""
        for f in obj.foto_set.all():
            thumbnail_url = get_thumbnailer(f.foto).get_thumbnail({
                'size': (50, 50),
                'crop': "center",
                'detail': True,
                }).url
            gal +=u"<img src='%s'> " % thumbnail_url
        return gal
    galeria.allow_tags = True
    galeria.short_description = "fotos da suite"

    def enviar_zip_de_fotos(self,request,query_set):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/evento/foto_upload/?ids=%s" % (",".join(selected)))

class FotoAdmin(ImageCroppingMixin,admin.ModelAdmin):
    pass

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nome_en','info', 'info_en','preco','ordem']
admin.site.register(Evento,EventoAdmin)
admin.site.register(Foto,FotoAdmin)
admin.site.register(Categoria,CategoriaAdmin)


# vim: set ts=4 sw=4 sts=4 expandtab:
