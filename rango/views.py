from django.http import HttpResponse
from django.shortcuts import render

from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page


# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    context = {
        'categories': category_list,
        'pages': pages_list
    }

    return render(request, 'rango/index.html', context=context)


def about(request):
    context = {
        'myname': 'Jesus'
    }

    return render(request, 'rango/about.html', context=context)


def show_category(request, category_name_slug):
    context = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context['pages'] = pages
        context['category'] = category
    except Category.DoesNotExist:
        context['pages'] = context['category'] = None

    return render(request, 'rango/category.html', context)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.filter(slug=category_name_slug)[0]
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context = {'form': form, 'category': category}

    return render(request, 'rango/add_page.html', context)
