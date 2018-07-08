from django.http import HttpResponse
from django.shortcuts import render


def posts_home(request):
	return HttpResponse('<h1>Home page Posts</h1>')
	# return render()
