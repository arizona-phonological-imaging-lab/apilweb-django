from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def printAppropriateRowOpeningTag(context, value):
    pageThickBorders = context['pageThickBorders']
    pageShaded = context['pageShaded']
    if value in pageThickBorders and value in pageShaded:
        return u"<div class='mainTableRow thickBottom shaded'>"
    elif value in pageThickBorders and value not in pageShaded:
        return u"<div class='mainTableRow thickBottom'>"
    elif value not in pageThickBorders and value in pageShaded:
        return u"<div class='mainTableRow shaded'>"
    else:
        return u"<div class='mainTableRow'>"