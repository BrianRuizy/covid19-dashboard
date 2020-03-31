from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from . import getdata

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


def report(request):
    daily_df = getdata.daily_report()
    return render(request, 'index.html', {
        'num_confirmed':daily_df.Confirmed.sum(),
        'num_recovered':daily_df.Recovered.sum(),
        'num_deaths':daily_df.Deaths.sum()
        })
