from rest_framework import serializers
from .models import Book

#모델의 데이터를 JSON문자열로 변환해서 출력하기위한
#Serializer 생성 
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['bid', 'title', 'author', 'category', 
                  'pages', 'price', 'published_date', 'description']