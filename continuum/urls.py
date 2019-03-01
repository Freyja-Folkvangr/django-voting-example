from django.conf.urls import url, include
from . import views

app_name = 'continuum'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^enter-project/$', views.enterProject, name='enterproject'),
	url(r'^detail-project/$', views.detailProject, name='detailproject'),
	url(r'^submitVote/$', views.submitVote, name='submitVote')
]