from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page


# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    context = {
        'categories': category_list,
        'pages': pages_list
    }

    visitor_cookie_handler(request)

    context['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context)

    return response


def about(request):
    context = {
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


@login_required
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


@login_required
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


@login_required
def restricted(request):
    return HttpResponse('You are not logged in!')


# Helper functions

def get_server_side_cookies(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits_cookie = int(get_server_side_cookies(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookies(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits_cookie = visits_cookie + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

        request.session['visits'] = visits_cookie
