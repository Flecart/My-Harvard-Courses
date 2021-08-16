from django import template
from markdown2 import Markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def markdown(mdfile):
    markdowner = Markdown()
    return mark_safe(markdowner.convert(mdfile))
    # return mdfile + " ciao"