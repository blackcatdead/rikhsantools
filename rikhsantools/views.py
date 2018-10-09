from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from rikhsantools.forms import FileForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rikhsantools.models import Photo
from fpdf import FPDF
from rikhsantools import settings
import img2pdf
import os
from django.core.files import File

def index(request):
	# path="MEDIA/profile/1"
	# img_list =os.listdir(path) 
	template = loader.get_template('imgtopdf.html')
	context = {
		'page': 'Dokumen',
		# 'files': img_list
	}
	return HttpResponse(template.render(context, request))

# @csrf_exempt
# def uploadFiles(request):
# 	form = FileForm(request.POST, request.FILES)
# 	if form.is_valid():
# 		print(form)
# 		if request.session.get('visitor') is None:
# 			# print('asdasdasdads')
# 			visitor = Visitor()
# 			visitor.save()
# 			request.session['visitor']= visitor.id_visitor
# 			# print(visitor)
# 		photo = form.save(commit=False)
# 		photo.visitor= Visitor.objects.get(id_visitor=request.session.get('visitor'))
# 		photo.save()
# 		singimagetopdf(photo)
# 		print(photo)
# 		data = {'is_valid': True, 'name': photo.photo.name, 'url': photo.photo.url, 'id_file': photo.id_photo}
# 	else:
# 	    data = {'is_valid': False}
# 	return JsonResponse(data)

# @csrf_exempt
# def uploadFiles(request):
# 	# form = UploadFileForm(request.POST, request.FILES)
# 	if request.FILES:
# 		if request.session.get('visitor') is None:
# 			visitor = Visitor()
# 			visitor.save()
# 			request.session['visitor']= visitor.id_visitor

# 		directory="MEDIA/pdf/"+str(request.session.get('visitor'))
# 		if not os.path.exists(directory):
# 			os.makedirs(directory)

# 		pdff = Pdf(visitor=Visitor.objects.get(id_visitor=request.session.get('visitor')))
# 		pdff.save()
# 		# print(request.FILES['photo'])
# 		pdf_bytes = img2pdf.convert([request.FILES['photo']])
# 		location='pdf/'+str(request.session.get('visitor'))+'/'+str(pdff.id_pdf)+'.pdf'
# 		file = open("MEDIA/"+location,"wb")
# 		file.write(pdf_bytes)
# 		file.close()
# 		pdff.pdf=location
# 		pdff.save()
# 		data = {'is_valid': True, 'name': pdff.pdf.name, 'url': pdff.pdf.url, 'id_file': pdff.id_pdf}
# 	else:
# 	    data = {'is_valid': False}
# 	return JsonResponse(data)
	
def imgtoPDF(imglist):
	pdf_bytes = img2pdf.convert(imglist)
	location='pdf/tesstt.pdf'
	file = open("media/"+location,"w")
	file.write(pdf_bytes)
	file.close()
	

# @csrf_exempt
# def uploadFiles(request):
# 	# form = UploadFileForm(request.POST, request.FILES)
# 	if request.FILES:
# 		img = request.FILES['photo']
# 		img_name = os.path.splitext(img.name)[0]
# 		img_extension = os.path.splitext(img.name)[1]
# 		user_folder = settings.MEDIA_ROOT+'/images'

# 		filename= ('%s%s' % (img_name, img_extension))
# 		img_save_path = ('%s/%s' % (user_folder, filename))
# 		cpy=0
# 		while os.path.exists(img_save_path):
# 			cpy=cpy+1
# 			filename = ('%s%s' % (img_name+"_"+str(cpy), img_extension))
# 			img_save_path = ('%s/%s' % (user_folder, filename))

# 		with open(img_save_path, 'wb+') as f:
# 			for chunk in img.chunks():
# 				 f.write(chunk)
# 		data = {'is_valid': True, 'name': filename,}
# 	else:
# 	    data = {'is_valid': False}
# 	return JsonResponse(data)

@csrf_exempt
def uploadFiles(request):
	form = FileForm(request.FILES,request.POST)
	if form.is_valid():
		f = form.save()
		img = request.FILES['photo']
		f.filename= os.path.splitext(img.name)[0]
		f.save()
		data = {'is_valid': True, 'name': f.filename, 'url': f.photo.url, 'id': f.id_photo}
	else:
	    data = {'is_valid': False}
	return JsonResponse(data)

def singleimgtopdf(request):
	photo = get_object_or_404(Photo, id_photo=request.GET['id'])
	imglist=[]
	imglist.append(photo.photo.path)
	pdf_bytes = img2pdf.convert(imglist)
	response = HttpResponse(pdf_bytes, content_type="application/pdf")
	response['Content-Disposition'] = 'attachment; filename='+photo.filename+'.pdf'
	return response

@csrf_exempt
def combinetopdf(request):
	print(request.POST)
	photos = Photo.objects.filter(id_photo__in=request.POST.getlist('ids[]'))
	imglist=[]

	for p in photos:
		# print(p.photo.path)
		imglist.append(p.photo.path)
	# for x in request.POST.getlist('ids[]'):
	# 	imglist.append('media/images/'+x)
	# 	print('media/images/'+x)
	pdf_bytes = img2pdf.convert(imglist)
	response = HttpResponse(pdf_bytes, content_type="application/pdf")
	response['Content-Disposition'] = 'attachment; filename=combined.pdf'
	return response

# def singleimagetopdf(photo):
# 	pdf = FPDF()
# 	# imagelist is the list with all image filenames
# 	pdf.add_page()
# 	pdf.image(photo.photo.path)
# 	pdf.output("MEDIA/pdf/"+str(photo.id_photo)+".pdf", "F")

# def imagestopdf(photos):
# 	pdf = FPDF()
# 	# imagelist is the list with all image filenames
# 	for image in photos:
# 	    pdf.add_page()
# 	    pdf.image(image.photo.path)
# 	pdf.output("yourfile.pdf", "F")


# def singimagetopdf(photo):
# 	directory="MEDIA/pdf/"+str(photo.visitor.id_visitor)
# 	if not os.path.exists(directory):
# 		os.makedirs(directory)

# 	pdf_bytes = img2pdf.convert([photo.photo.path])

# 	file = open("MEDIA/pdf/"+str(photo.visitor.id_visitor)+"/"+str(photo.id_photo)+".pdf","wb")
# 	file.write(pdf_bytes)
from io import StringIO
from PyPDF2 import PdfFileMerger, PdfFileReader
def mergepdf(request):
	merger = PdfFileMerger()
	pdfs = Pdf.objects.filter(visitor=Visitor.objects.get(id_visitor=request.session.get('visitor')))
	for filename in pdfs:
		print('media/'+filename.pdf.name)
		merger.append(filename.pdf.path)
	outputStream = StringIO.StringIO()
	merger.write(outputStream)
	response = HttpResponse(content_type="application/pdf")
	response['Content-Disposition'] = 'attachment; filename=combined.pdf'
	response.write(outputStream.getvalue())
	return response



