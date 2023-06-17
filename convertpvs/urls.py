from django.urls import path
from . import tasks
from .views import get_all_data, download_zip_files, view_file,convertfiles, download_file


urlpatterns = [
    # path('', files),

    path('', get_all_data, name='index'),
    path('<str:file>/<str:view>/', view_file),  # to read
    path('schedule/', tasks.schedule, name="schedule"),  # schedular
    path('convert/', convertfiles, name='convertfiles'),  # Convert File
    path('downloadzip/', download_zip_files, name='download_zip_files'), # download zip file
    path('<str:file>/<str:view>/<str:viewr3>/', download_file,name='downloadsinglefile'),  # to download

    # path('fileconverter/', fileConverion, name='fileconverter'),

    # path('conversion/s', files, name='files'),
    # path('fileconverter/<str: file>/<str: view>/', view_file),


]