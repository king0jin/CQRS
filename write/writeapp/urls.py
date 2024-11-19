from django.urls import path
from .views import helloAPI

urlpatterns = [
    #hello/ 요청시 현재 디렉토리의 views파일의 helloAPI함수 호출
    path("hello/", helloAPI),
]