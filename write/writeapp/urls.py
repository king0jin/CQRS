from django.urls import path
from .views import helloAPI, bookAPI

urlpatterns = [
    #hello/ 요청시 현재 디렉토리의 views파일의 helloAPI함수 호출
    path("hello/", helloAPI),
    #CQRS - 삽입요청 : book/요청시 현재 디렉토리의 views파일의 bookAPI함수 호출
    path('book/', bookAPI),
]