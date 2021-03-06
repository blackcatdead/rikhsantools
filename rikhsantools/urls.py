"""rikhsantools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from rikhsantools import views as v
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
	# path('imgtopdf/', v.index, name='imgtopdf'),
    path('admin/', admin.site.urls),

    path('proc/upload/files', v.uploadFiles, name='uploadfiles'),
    path('proc/singleimgtopdf', v.singleimgtopdf, name='singleimgtopdf'),
    path('proc/combinetopdf', v.combinetopdf, name='combinetopdf'),

    path('proc/upload/pdfscombine', v.pdfscombine_upload, name='pdfscombine_upload'),
    path('proc/pdfscombine/combine', v.pdfscombine_combine, name='pdfscombine_combine'),

]

from django.conf.urls.i18n import i18n_patterns
urlpatterns += i18n_patterns( # < here
    # path('', include('base.urls'))
    path('', include('rikhsantools.urlslang')),
    # prefix_default_language=False,
) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)