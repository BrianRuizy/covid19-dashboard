from django import template

register = template.Library()

GREEN = "text-success"
RED = "text-danger"

ARROW_UP = "fa fa-angle-up"
ARROW_DOWN = "fa fa-angle-down"

CONDITIONS = {
    'death_rate': {
        "GT_0": (RED, ARROW_UP),
        "LT_0": (GREEN, ARROW_DOWN)
    },
    'recovered': {
        "GT_0": (GREEN, ARROW_UP),
        "LT_0": (RED, ARROW_DOWN)
    },
    'confirmed': {
        "GT_0": (RED, ARROW_UP),
        "LT_0": (GREEN, ARROW_DOWN)
    },
    'deaths': {
        "GT_0": (RED, ARROW_UP),
        "LT_0": (GREEN, ARROW_DOWN)
    },
}


@register.simple_tag
def arrow(name, value):
    if value > 0:
        return CONDITIONS[name]["GT_0"][1]
    else:
        return CONDITIONS[name]["LT_0"][1]


@register.simple_tag
def color(name, value):
    if value > 0:
        return CONDITIONS[name]["GT_0"][0]
    else:
        return CONDITIONS[name]["LT_0"][0]



