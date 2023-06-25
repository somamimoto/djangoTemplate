from django.shortcuts import render, redirect
from .models.cat_models import CatZukan
from .models.dog_models import DogZukan
from django.http import HttpResponse


def index(request, category_slug):
    if category_slug in ['dog', 'cat']:
        if category_slug == 'dog':
            zukan = DogZukan.objects.filter(is_public=True)
        else:
            zukan = CatZukan.objects.filter(is_public=True)
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
