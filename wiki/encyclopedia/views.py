from django.shortcuts import render
import markdown
import random
from . import util

def converter_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content_html = converter_to_html(title)
    if content_html == None:
        return render(request, "encyclopedia/error.html", {
        "errormessage":"This Entry does not exist yet."    
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content": content_html
        })

def search(request):
    if request.method == "POST":
        index_search = request.POST['q']
        content_html = converter_to_html(index_search)
        if content_html is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": index_search,
                "content": content_html
            })
        else:
            entries = util.list_entries()
            closeResults = []
            for entry in entries:
                if index_search.lower() in entry.lower():
                    closeResults.append(entry)
            return render(request, "encyclopedia/search.html", {
                "closeResults": closeResults
            })
            
def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        if_title_present = util.get_entry(title)
        if if_title_present is not None:
            return render(request, "encyclopedia/error.html", {
                "errormessage": "This page already exists"
            })
        else:
            util.save_entry(title, content)
            content_html = converter_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content_html
            })
            
def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
             "title": title,
             "content": content
         })
        
def save_edit(request):
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST ['content']
            util.save_entry(title, content)
            content_html = converter_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content_html
            })
            
def random_function(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    content_html = converter_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": content_html
    })