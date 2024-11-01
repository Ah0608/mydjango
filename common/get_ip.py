def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # 取第一个IP，即客户端的真实IP
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # 如果没有代理，直接获取 REMOTE_ADDR
        ip = request.META.get('REMOTE_ADDR')
    return ip
