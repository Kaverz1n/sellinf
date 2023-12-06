from django import template

from users.models import User

register = template.Library()


@register.filter
def mediapath(url: str) -> str:
    '''
    Return media url for media file
    :return: media url
    '''
    media_url = f'/media/{url}'
    return media_url


@register.filter
def has_group(user: User, group_name: str) -> bool:
    '''
    Return bool-value if user belongs to the group
    :param user: current user
    :param group_name: group name
    :return: bool-value
    '''
    return user.groups.filter(name=group_name).exists()
