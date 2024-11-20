from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 삽입 요청 처리를 하기위한 라이브러리 import
from .models import Book
from .serializers import BookSerializer
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def helloAPI(request):
    return Response("hello jini~") 

#CQRS - 삽입요청
@api_view(['POST'])
def bookAPI(request):
    #요청받은 데이터
    data = request.data
    data['pages'] = int(data['pages'])
    data['price'] = int(data['price'])
    #데이터 직렬화 
    serializer = BookSerializer(data=data)
    #직렬화를 한 데이터가 유효한 값이라면
    if(serializer.is_valid()):
        #저장한다
        serializer.save()
        #결과 반환
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

