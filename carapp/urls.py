from django.urls import path
from .views import *

app_name = 'carapp'

urlpatterns = [
    path('center', get_center, name='get_center_data'),
    path('center/scrolldata', get_scrolldata, name='get_scrolldata'),
    path('center/ratio', get_ratio, name='get_ratio'),
    path('left', get_left, name='get_left'),
    path('right', get_right, name='get_right'),
    path('bottom/left', get_bottom_left, name='get_bottom_left'),
    path('bottom/right', get_bottom_right, name='get_bottom_right'),
]