from django import template

register = template.Library()

@register.simple_tag
def my_url(value, field_name, urlencode=None): #value will pass page number, field_name pass string page and URL
    url = f'?{field_name}={value}'

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0]!=field_name, querystring) #take query string list, take each string and split it by 2, if the first string is equel to the field.
        encoded_querystring = '&'.join(filtered_querystring)
        url = f'{url}&{encoded_querystring}'

    return url