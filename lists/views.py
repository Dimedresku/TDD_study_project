from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import FormView, CreateView

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm

User = get_user_model()


class HomePageView(FormView):
    '''home page'''
    template_name = 'home.html'
    form_class = NewListForm


def view_list(request, list_id):
    '''list view'''
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(data=request.POST, for_list=list_)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


class NewListView(CreateView, HomePageView):
    def form_valid(self, form):
        list_ = form.save(owner=self.request.user)
        return redirect(list_)


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})
