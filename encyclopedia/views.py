from django.shortcuts import render, redirect
from . import util
from markdown2 import markdown
from django.http import HttpResponseRedirect
from random import randint

from .models import Data

def index(request):
    st = list(Data.objects.values_list('title', flat=True))
    return render(request, "encyclopedia/index.html", {
        "entries": st
    })

def entry(request,name):
    content = Data.objects.filter(title=name).first()
    if content is not None:
        return render(request, "encyclopedia/display.html", {
            "entries": markdown(content.body), "title":name
        })
    else:
        return render(request,"encyclopedia/page_not.html")

def search(request):
    entries = list(Data.objects.values_list('title', flat=True))
    query = request.GET.get("q", "")
    if query in entries:
        return HttpResponseRedirect(f'{query}')
    results = [entry for entry in entries if query.lower() in entry.lower()]
    if results:
        return render(request, "encyclopedia/search.html", {
            "entries": results,
        })
    else:
        return render(request,"encyclopedia/page_not.html"         
        )

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        l = Data.objects.filter(title=title)
        if len(l) == 0:
            Data(title=title, body=content).save()
            return HttpResponseRedirect(f'{title}')
        else:
            return render(request, "encyclopedia/page_not.html")
    return render(request, "encyclopedia/Create.html")

def edit(request, name):
    if request.method == "POST":
        title = name
        content = request.POST.get("content")
        data = Data.objects.get(title=name)
        data.body = content
        data.save()
        return redirect(entry, title)
    return render(request, "encyclopedia/edit.html",{
        "title":name, "content": Data.objects.get(title=name).body
    })

def random(request):
    list1 = list(Data.objects.values_list('title', flat=True))
    t1=randint(0,len(list1)-1)
    return redirect(entry,list1[t1]) 



