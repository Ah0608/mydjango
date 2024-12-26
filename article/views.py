import re

import markdown
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from common.my_paginator import pg
from mydjango.settings import mark_config
from .forms import ArticleForm
from .models import Article


@login_required
def article_list(request):
    user = request.user
    queryset = Article.objects.all().filter(author_id=user.id,is_delete=False).order_by('-id')
    page_obj, page_range = pg(queryset, request, 5)

    return render(request, 'articlelist.html', {'page_obj': page_obj, 'page_range': page_range, 'user': user})


@login_required
def article_create(request):
    user = request.user
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        image = request.FILES.get('editormd-image-file')
        if form.is_valid():
            article = form.save(commit=False)
            article.author = user
            article.save()
            return redirect('article_list')  # 重定向到显示所有文章的页面
    else:
        form = ArticleForm()
        return render(request, 'articlecreate.html', locals())


@login_required
def article_detail(request, pk):
    user = request.user
    article = Article.objects.filter(id=pk, author_id=user.id).first()

    # 获取前一篇文章的 id
    previous_article = Article.objects.filter(id__gt=pk,is_delete=False).order_by('id').first()
    previous_article_obj = previous_article if previous_article else None

    # 获取后一篇文章的 id
    next_article = Article.objects.filter(id__lt=pk,is_delete=False).order_by('-id').first()
    next_article_obj = next_article if next_article else None

    article.content = markdown.markdown(article.content, extensions=mark_config)
    n = article.content.count('<div class="codehilite">', 0, len(article.content))
    for i in range(n):
        article.content = re.sub(r'<div class="codehilite">',
                                 '<button id="copybtn{}" class="copybtn" data-clipboard-action="copy" data-clipboard-target="#code{}">复制</button>'
                                 '<div class="codehilite" id="code{}">'.format(
                                     i, i, i), article.content, 1)
    data_dict = {'article': article, 'user': user, 'previous_article_obj': previous_article_obj,
                 'next_article_obj': next_article_obj}
    return render(request, 'articledetail.html', data_dict)


@login_required
def article_edit(request, pk):
    user = request.user
    article = Article.objects.filter(id=pk, author_id=user.id).first()
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articleedit.html', {'form': form})


@login_required
def article_delete(request, pk):
    user = request.user
    obj = Article.objects.filter(id=pk, author_id=user.id)
    obj.update(is_delete=True)
    return redirect('article_list')


@login_required
def article_search(request):
    user = request.user
    keyword = request.POST.get('query', None)
    queryset = Article.objects.all().filter(title__icontains=keyword).order_by('-created_at')

    page_obj, page_range = pg(queryset, request, 5)
    return render(request, 'articlelist.html', {'page_obj': page_obj, 'page_range': page_range, 'user': user})
