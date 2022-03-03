from django.shortcuts import render
from django.http import HttpResponse
import os

def index(request):
	return render(
		request,
		'./index.html',
		{ "images": os.listdir("images") }
	)

def image(request, imagename):
	image_data = open("./images/%s.jpg" % imagename, "rb").read()
	return HttpResponse(image_data, content_type="image/png")
