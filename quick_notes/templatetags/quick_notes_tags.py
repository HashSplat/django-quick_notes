from django import template
register = template.Library()


@register.inclusion_tag('quick_notes/quick_note.html')
def quick_note_card(quick_note):
    return {'quick_note': quick_note}
