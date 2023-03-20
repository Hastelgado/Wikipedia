from django.shortcuts import render
from django.http import HttpResponse

from . import util
from markdown2 import Markdown
import random

markdown = Markdown()

def index(request):
    if request.method == "POST":
        entries = [x.lower() for x in util.list_entries()]
        query = str(request.POST.get("q")).lower()
        if query in entries:
            content = markdown.convert(util.get_entry(query))
            return render(request, "encyclopedia/search.html", {
                "content": content, "title": query,
            })
        else:
            list=[]
            for i in range(len(entries)):
                if (query in entries[i]) or (str(entries[i]).startswith(query)):
                    list.append(entries[i])
            searchlist = [x.capitalize() for x in list]
            return render(request, "encyclopedia/search.html", {
                "searchlist": searchlist,
            })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def page(request, page):
    if util.get_entry(page):

        content = markdown.convert(util.get_entry(page))
        return render(request, "encyclopedia/search.html", {
                "content": content, "title": str(page).lower(),
            })

    else:
        
        return HttpResponse("<h1 style='color:blue'>Your requested page was not found. Please input an existing directory.</h1>")
    

def newpage(request):

    if request.method == "POST":
        title = request.POST.get("title")
        textarea = request.POST.get("textarea")

        if util.get_entry(title):
            return HttpResponse("<h1 style='color:blue'>This page title already exists! Choose a different one.</h1>")
        
        util.save_entry(title, textarea)
        return render(request, "encyclopedia/search.html",{
            "content": markdown.convert(textarea), "title": str(title).lower(),
        } )

    else:
        return render(request, "encyclopedia/newpage.html")


def editpage(request):

    if request.method == "POST":
        
        title = request.POST.get("title")
        textarea = request.POST.get("textarea")

        util.save_entry(str(title).capitalize(), textarea)

        return render(request, "encyclopedia/search.html",{
            "content": markdown.convert(textarea), "title": title,
        } )
    

    else:
        title = request.GET.get("title")
        contents = util.get_entry(title)
        print(contents)
        return render(request, "encyclopedia/editpage.html",{
            "content": contents, "title": str(title).lower(),
        })


def randompage(request):

    randompage = random.choice(util.list_entries())
    content = util.get_entry(randompage)
    return HttpResponse(markdown.convert(content))