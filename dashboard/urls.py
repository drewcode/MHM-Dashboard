from django.urls import re_path 
from dashboard import views

urlpatterns = [
    re_path(r'^api/data$', views.data_list),
    re_path(r'^api/data/(?P<pk>[0-9]+)$', views.data_detail),
    re_path(r'^api/data/(?P<d_id>[\w]+)/(?P<date>[\d]+-[\d]+)$', views.patient_day_data)
]