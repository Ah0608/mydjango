from django.core.paginator import Paginator


def pg(queryset,request,page):
    paginator = Paginator(queryset, page)  # 每页显示10条数据

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取当前页码和总页数
    current_page = page_obj.number
    total_pages = paginator.num_pages

    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    elif current_page <= 3:
        page_range = range(1, 6)
    elif current_page >= total_pages - 2:
        page_range = range(total_pages - 4, total_pages + 1)
    else:
        page_range = range(current_page - 2, current_page + 3)

    return page_obj,page_range