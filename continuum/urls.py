from django.conf.urls import url, include
from django.urls import path
from . import views

app_name = 'continuum'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_choice/$', views.create_choice, name='create_choice'),
    url(r'^view_choices/$', views.view_choices, name='view_choices'),
    path('<int:choice_id>/view_choice_details/', views.view_choice_details, name='view_choice_details'),
    url(r'^submitVote/$', views.submitVote, name='submitVote'),
    url(r'^create_question/$', views.create_question, name='create_question'),

    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('questions/latest/', views.index),
]
