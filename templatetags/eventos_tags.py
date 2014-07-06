from django import template
register = template.Library()


from eventos.models import Evento


@register.inclusion_tag('eventos/ciclo-eventos.html', takes_context=True)
def ciclo_eventos(context):
    request = context['request']
    return {'eventos': Evento.objects.da_unidade(request)}

