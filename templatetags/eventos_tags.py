from django import template
register = template.Library()


from appfotos.models import Evento, Categoria


@register.inclusion_tag('eventos/ciclo-eventos.html', takes_context=True)
def ciclo_eventos(context):
    request = context['request']
    return {'eventos': Evento.objects.all()}

@register.inclusion_tag('eventos/tipos-suites.html', takes_context=True)
def tipos_suites(context):
    request = context['request']
    return {'tipos': Categoria.objects.all()}

