from django.urls import path
from .views import bookAPI

urlpatterns = [
    #books/ 요청시 현재 디렉토리의 views파일의 bookAPI함수 호출
    path("books/", bookAPI),
]