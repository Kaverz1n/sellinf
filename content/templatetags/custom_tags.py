from django import template

register = template.Library()


@register.filter
def mediapath(url: str) -> str:
    '''
    Return media url for media file
    :return: media url
    '''
    media_url = f'/media/{url}'
    return media_url
