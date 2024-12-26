from django import template

register = template.Library()

# 定义数字到汉字的映射
num_to_chinese = {
    1: '一', 2: '二', 3: '三', 4: '四',
    5: '五', 6: '六', 7: '七', 8: '八', 9: '九'
}


def arabic_to_chinese(num):
    if not isinstance(num, int):
        raise ValueError("Input must be an integer.")

    if num == 0:
        return num_to_chinese[0]

    result = []
    for digit in str(num):
        result.append(num_to_chinese[int(digit)])

    return ''.join(result)


@register.filter
def number_to_chinese(value):
    try:
        return arabic_to_chinese(int(value))
    except ValueError:
        return value
