from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from rikhsantools.forms import FileForm, PdfscombineForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rikhsantools.models import Imagetopdf, Pdfscombine
from fpdf import FPDF
from rikhsantools import settings
import img2pdf
import os
from django.core.files import File
from django.core.exceptions import ValidationError

def home (request):
	template = loader.get_template('home.html')
	context = {
		'page': 'Home',
	}
	return HttpResponse(template.render(context, request))


def tool_imgtopdf(request):
	template = loader.get_template('imgtopdf.html')
	context = {
		'page': 'Image to PDF',
	}
	return HttpResponse(template.render(context, request))

@csrf_exempt
def uploadFiles(request):
	form = FileForm(request.POST, request.FILES)
	if form.is_valid():
		f = form.save()
		img = request.FILES['image']
		f.filename= os.path.splitext(img.name)[0]
		f.save()
		data = {'is_valid': True, 'name': f.filename, 'url': f.image.url, 'id': f.id_imagetopdf}
	else:
	    data = {'is_valid': False, 'name': str(request.FILES['image']), 'url': '', 'id': ''}
	return JsonResponse(data)

def singleimgtopdf(request):
	imagetopdf = get_object_or_404(Imagetopdf, id_imagetopdf=request.GET['id'])
	imglist=[]
	imglist.append(imagetopdf.image.path)
	pdf_bytes = img2pdf.convert(imglist)
	response = HttpResponse(pdf_bytes, content_type="application/pdf")
	response['Content-Disposition'] = 'attachment; filename='+imagetopdf.filename+'.pdf'
	return response

@csrf_exempt
def combinetopdf(request):
	print(request.POST)
	photos = Imagetopdf.objects.filter(id_imagetopdf__in=request.POST.getlist('ids[]'))
	imglist=[]
	for p in photos:
		imglist.append(p.image.path)
	pdf_bytes = img2pdf.convert(imglist)
	response = HttpResponse(pdf_bytes, content_type="application/pdf")
	response['Content-Disposition'] = 'attachment; filename=combined.pdf'
	return response


# END imagetopdf

def tool_pdfscombine(request):
	template = loader.get_template('pdfscombine.html')
	context = {
		'page': 'PDFs Combine',
	}
	return HttpResponse(template.render(context, request))

@csrf_exempt
def pdfscombine_upload(request):
	form = PdfscombineForm(request.POST, request.FILES)
	valid_extensions = ['.pdf']
	if form.is_valid() and os.path.splitext(str(request.FILES['pdf']))[1] in valid_extensions:
		f = form.save()
		img = request.FILES['pdf']
		f.filename= os.path.splitext(img.name)[0]
		f.save()
		data = {'is_valid': True, 'name': f.filename, 'url': f.pdf.url, 'id': f.id_pdfscombine}
	else:
	    data = {'is_valid': False, 'name': str(request.FILES['pdf']), 'url': '', 'id': ''}
	return JsonResponse(data)

from PyPDF2 import PdfFileMerger, PdfFileReader
@csrf_exempt
def pdfscombine_combine(request):
	print(request.POST)
	pdfs = Pdfscombine.objects.filter(id_pdfscombine__in=request.POST.getlist('ids[]'))
	merger = PdfFileMerger()
	for p in pdfs:
		merger.append(open(p.pdf.path, 'rb'))
	# pdf_bytes = merger.write("document-output.pdf")
	# response = HttpResponse(merger, content_type="application/pdf")
	

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=combined.pdf'
	merger.write(response)
	return response