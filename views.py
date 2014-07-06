from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.views.generic import View,DetailView
from django.conf import settings
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import tempfile
import os
import zipfile
import shutil

from eventos.models import Evento, Foto

class UploadFotoForm(forms.Form):
    ids = forms.CharField(max_length=50)
    file  = forms.FileField()
   
class FotoUploadView(View):
    def get(self, request):
        form = UploadFotoForm(initial={'ids':request.GET.get('ids')})
        form.fields['ids'].widget = forms.HiddenInput()
        response = render(request,'eventos/foto_upload.html',{'form':form})
        return response

    def post(self,request):
        form = UploadFotoForm(request.POST, request.FILES)
        if form.is_valid():
            self.handle_uploaded_file(request.FILES['file'],form)
        return HttpResponseRedirect('/admin/eventos/evento/')

    def handle_uploaded_file(self,f,form):
        ids = form.cleaned_data['ids'].split(',')
        pasta_temp = tempfile.mkdtemp()
        file_temp = os.path.join(pasta_temp,ids[0]+".zip")

        with open(file_temp, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
       
        # criando pasta temporaria para salvar os unzip
        unzip_pasta = os.path.join(pasta_temp,"unzip")
        if not os.path.exists(unzip_pasta):
            os.makedirs(unzip_pasta)
        unzip(file_temp,unzip_pasta)

        # salvando novos arquivos usando a pasta temporaria
        evento = Evento.objects.get(id=ids[0])
        for name in os.listdir(unzip_pasta):
            fi = os.path.join(unzip_pasta,name)
            if os.path.isfile(fi):
                with open(fi) as foto_file:
                    foto = Foto(evento=evento,foto=File(foto_file))
                    foto.save()
        #shutil.rmtree(unzip_pasta)

class EventosView(View):
    def get(Self,request):
        eventos = Evento.objects.da_unidade(request)
        paginator = Paginator(eventos,18)
        page = request.GET.get('page')
        try:
            eventos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            eventos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            eventos = paginator.page(paginator.num_pages)

        categorias = {}
        for e in eventos:
            if e.categoria:
                categorias[e.categoria.id]=e.categoria

        return render(request,'eventos/eventos.html',{'eventos':eventos,'categorias':categorias})

class EventoView(DetailView):
    model = Evento
    template_name= "eventos/evento.html" 

def unzip(zipFilePath, destDir):
    #os.system('cd %s; unzip -f %s' % (destDir,zipFilePath))
    zfile = zipfile.ZipFile(zipFilePath)
    zfile.extractall(destDir)
