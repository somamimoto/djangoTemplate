from django.shortcuts import render, redirect
from .models.cat_models import CatZukan
from .models.dog_models import DogZukan
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request, category_slug):
    if category_slug in ['dog', 'cat']:
        if category_slug == 'dog':
            zukan = DogZukan.objects.filter(is_public=True)
        else:
            zukan = CatZukan.objects.filter(is_public=True)
        page = request.GET.get('page', 1)
        paginator = Paginator(zukan, per_page=5, orphans=2)
        # We have implemented try-except clause as django original source code does
        # https://github.com/django/django/blob/main/django/core/paginator.py
        try:
            zukan = paginator.page(page)
        except PageNotAnInteger:
            zukan = paginator.page(1)
        except EmptyPage:
            zukan = paginator.page(paginator.num_pages)
        context = {
            'category': category_slug,
            'zukan': zukan,
            }
        return render(request, 'zukan/index.html', context)
    return redirect('home')


def detail(request, category_slug, slug):
    if category_slug in ['dog', 'cat']:
        if category_slug == 'dog':
            obj = DogZukan.objects.get(slug__exact=slug)
        else:
            obj = CatZukan.objects.get(slug__exact=slug)
        context = {
            'obj': obj,
            }
        return render(request, 'zukan/detail.html', context)
    return redirect('home')
