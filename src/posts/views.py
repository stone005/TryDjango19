from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import Postform
from .models import Post


def post_create(request):
    form = Postform(request.POST or None, request.FILES or None)

    # POST mi aggiunge i dati della form e None non mi fa vedere la scritta 'campo obbligatorio' nel caricamento
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'Successfully created')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'post_form.html', context)


def post_detail(request, slug=None):
    # instance = Post.objects.get(id=8)
    instance = get_object_or_404(Post, slug=slug)
    # in Instance metto l'oggetto o faccio vedere una pagina di errore il cui id è id
    context = {
        'title':instance.title,
        'instance': instance
    }
    # context sono i dati da passare alla form, in questo caso con un dizionario
    return render(request, 'post_detail.html', context)


def post_list(request):
    queryset_list = Post.objects.all() # .order_by('-timestamp')
    paginator = Paginator(queryset_list, 10) # Show 10 posts per page
    page_request_var = 'page' # variabile per inserire la pagina a cui anre direttamente
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    # Query di tutti i post
    context = {
        'object_list': queryset,
        'title':'List',
        'page_request_var': page_request_var
    }
    return render(request, 'post_list.html', context)
    # ritorno il template(post_list.html) con i dati(context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = Postform(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'Item Saved!')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'post_form.html', context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request,'Successfully Deleted')
    return redirect('list')


