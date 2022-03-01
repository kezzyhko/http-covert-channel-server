from django.shortcuts import render

def index(request):
	images = ["test1", "test2"]
	return render(request, './index.html', {"images": images})