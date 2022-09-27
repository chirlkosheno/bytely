from random import random
from sqlite3 import IntegrityError
import string
from django.shortcuts import render, get_object_or_404, redirect
import hashlib
from .forms import UrlForm
from .models import Url


SHORT_URL_LEN = 7
ADD_RETRIES = 128


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def make_short_url(full_url):
    return hashlib.sha224(full_url.encode("utf-8")).hexdigest()[:SHORT_URL_LEN]


def try_add_url_to_bd(full_url):
    short_url = make_short_url(full_url)
    url = Url.objects.filter(short_url=short_url).first()
    if url is not None:
        if url.full_url == full_url:
            return short_url
    url_suffix = ''
    for _ in range(ADD_RETRIES):
        try:
            url = Url()
            url.full_url = full_url
            url.short_url = short_url
            url.save()
            return short_url
        except IntegrityError as e:
            url_suffix += randomword(SHORT_URL_LEN)
            short_url = make_short_url(full_url + url_suffix)


def index(request):
    short_url = None
    form = UrlForm()
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            full_url = form.cleaned_data['full_url']
            short_url = try_add_url_to_bd(full_url)

    if short_url:
        short_url = request.build_absolute_uri(f'/{short_url}')

    context = {
        'form': form,
        'short_url': short_url,
    }
    return render(request, 'index.html', context)


def redirector(request, short_url):
    url = get_object_or_404(Url, short_url=short_url)
    return redirect(url.full_url)

# Create your views here.
