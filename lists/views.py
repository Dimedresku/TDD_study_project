from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

def home_page(request):
    '''home page'''
    new_item_text = ''
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/lists/unique_url/')
    return render(request, 'home.html')

def view_list(request):
    '''list view'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
