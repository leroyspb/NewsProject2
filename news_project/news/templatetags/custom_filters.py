from django import template

register = template.Library()

censor_list = ['почти', 'хорошего', 'честность', 'главного']


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    """
    value: значение, к которому нужно применить фильтр
    """
    for word in censor_list:
        value = value.replace(word[1:], '*' * len(word[1:]))
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} '