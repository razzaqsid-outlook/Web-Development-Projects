from turtle import width
from attr import attrs
from django.http import HttpResponse,HttpResponseRedirect
from requests import request
from . import util
import markdown2
from django import forms
from django.shortcuts import render
from django.urls import reverse
from random import choice

def search_title(name):
    lines = util.get_entry(name)
    if lines != None:
        html = markdown2.markdown(lines)
        return (html)
    else:
        return lines


class SearchBar(forms.Form):
    query = forms.CharField(label="",widget=forms.TextInput({ "placeholder": "Search Encyclopedia"}))

class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    textarea = forms.CharField(label="Markdown Content",widget=forms.Textarea)

class EditEntry(forms.Form):
    textarea = forms.CharField(label="Markdown Content",widget=forms.Textarea)

def index(request):
        return render(request, "encyclopedia/index.html",{
            "entries": util.list_entries(),
            "form":SearchBar()
        })

def title(request, name):
    html = search_title(name)
    if html == None:
        edit_opt = False
        return render(request,"encyclopedia/entry.html",
        {
            "Edit":edit_opt,
            "name":name,
            "form":SearchBar()
        })
    else:
        edit_opt = True
        return render(request,"encyclopedia/entry.html",
        {
            "Edit":edit_opt,
            "html_code":html,
            "form":SearchBar(),
            "name":name,
        })

def search_bar(request):
    if request.method == "POST":
        form = SearchBar(request.POST)
        if form.is_valid():
            entry = form.cleaned_data.get("query")
            html = search_title(entry)
            if html == None:
                list = util.list_entries()
                list2 = []
                for item in list:
                    if entry in item:
                        list2.append(item)
                return render(request, "encyclopedia/search_results.html",{
                "entries": list2,
                "form":SearchBar()
                })
            else:
                return HttpResponseRedirect(reverse('encyclopedia:title',args=(entry,)))
    else:
        return render(request, "encyclopedia/index.html",{
            "entries": util.list_entries(),
            "form":SearchBar()
        })

def New_Entry(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            markdown = form.cleaned_data.get("textarea")
            exist = util.get_entry(title)
            if exist == None:
                util.save_entry(title,markdown)
                return HttpResponseRedirect(reverse('encyclopedia:title',args=(title,)))
            else:
                return render(request,"encyclopedia/entry.html",
                {
                    "html_code":"ERROR! Page Already Exist.",
                    "form":SearchBar()
                })
    else:
        return render(request,"encyclopedia/New_Entry.html",
        {
            "new_entry":NewEntry(),
            "form":SearchBar()
        })

def Edit_Entry(request,name):
    if request.method == "POST":
        form = EditEntry(request.POST)
        if form.is_valid():
            markdown = form.cleaned_data.get("textarea")
            util.save_entry(name,markdown)
            return HttpResponseRedirect(reverse('encyclopedia:title',args=(name,)))
    else:
        return render(request,"encyclopedia/Edit_Entry.html",
        {
            "title":name,
            "edit_entry":EditEntry(initial={'textarea':util.get_entry(name)}),
            "form":SearchBar()
        })

def Random_Entry(request):
    list = util.list_entries()
    title = choice(list)
    return HttpResponseRedirect(reverse('encyclopedia:title', args=(title, )))