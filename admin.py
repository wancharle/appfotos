from django.contrib import admin
from django.http import HttpResponseRedirect
from eventos.models import Evento, Foto, Categoria

from image_cropping import ImageCroppingMixin
from easy_thumbnails.files import get_thumbnailer


class FotoInline(admin.TabularInline):
    model = Foto
    fields = ('foto','legenda')

class EventoAdmin(ImageCroppingMixin,admin.ModelAdmin):
    inlines = [FotoInline,] 
    actions = ['enviar_zip_de_fotos',]

    def enviar_zip_de_fotos(self,request,query_set):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/evento/foto_upload/?ids=%s" % (",".join(selected)))

class FotoAdmin(ImageCroppingMixin,admin.ModelAdmin):
    pass

admin.site.register(Evento,EventoAdmin)
admin.site.register(Foto,FotoAdmin)
admin.site.register(Categoria)
