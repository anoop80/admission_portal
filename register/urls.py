__author__ = 'zeroonehacker'

from django.conf.urls import url
from register import views
#from wkhtmltopdf.views import PDFTemplateView
urlpatterns  = [
    #url(r'^$', views.register, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^prg', views.prg, name="prg"),
    url(r'^select_prg/', views.select_prg, name="select_prg"),
    url(r'^phd/', views.phd, name='phd'),
    url(r'^pg/', views.pg, name='pg'),
    url(r'^loggedin/',views.loggedin, name='loggedin'),
    url(r'^registered/',views.registered, name='registered'),
    url(r'^change_password/', views.change_pass,name="change_pass"),
    url(r'^form', views.registrationForm, name="Registration"),
    url(r'^logout/',views.logout,name='logout'),
    #url(r'^part_form/', views.pg, name="form"),
    url(r'^view_formpg/',views.view_formpg, name="view_formpg"),
    url(r'^view_formphd/',views.view_formphd, name="view_formphd"),	
    url(r'^pdf/$',views.generate_pdf,name='generate_pdf'),
    url(r'^pdf2/$',views.generate_pdf2,name='generate_pdf2'),

    #url(r'^form/', views.forms, name='main_form'),
    #url(r'^login/', views.login, name='login'),
]
