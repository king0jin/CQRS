#데이터 동기화를 위한 Kafka연결
import sys
import six
#Python 3.12 환경에서도 kafka-python 작동
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
      
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, KafkaError
import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 삽입 요청 처리를 하기위한 라이브러리 import
from .models import Book
from .serializers import BookSerializer
from rest_framework import status

#Kafka : 메세지송신 - MessageProducer클래스 생성
class MessageProducer:
    #초기화 메서드
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        #key_serializer=str.encode를 추가하여 key와 함께 전송할 메세지 준비
        self.producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            acks='all',
            api_version=(2, 5, 0),
            key_serializer=str.encode,
            retries=5,
            max_in_flight_requests_per_connection=5,
        )
    #메세지를 전송하는 메서드 
    def send_message(self, msg, auto_close=True):
        try:
            print(self.producer)
            future = self.producer.send(self.topic, value=msg, key="key")
            self.producer.flush() #비우는 작업
            if auto_close:
                self.producer.close()
            future.get(timeout=2)
            return {"status_code": 200, "error": None}
        except KafkaTimeoutError as e:
            print(f"KafkaTimeoutError: {e}")
            return {"status_code": 408, "error": "Request Timeout"}
        except KafkaError as e:
            print(f"KafkaError: {e}")
            return {"status_code": 500, "error": "Kafka Error"}
        except Exception as exc:
            print(f"Unexpected error: {exc}")
            raise

# Create your views here.
@api_view(['GET'])
def helloAPI(request):
    return Response("hello jini~") 

#CQRS - 삽입요청
@api_view(['POST'])
def bookAPI(request):
    try:
        #요청받은 데이터
        data = request.data
        data['pages'] = int(data['pages'])
        data['price'] = int(data['price'])
    except ValueError:
        return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)
    #데이터 직렬화 
    serializer = BookSerializer(data=data)
    #직렬화를 한 데이터가 유효한 값이라면
    if(serializer.is_valid()):
        #저장한다
        serializer.save()
        #삽입에 성공한 경우 카프카에게 메세지를 전송 준비
        #브로커와 토픽명을 지정
        broker = ["localhost:9092"]
        topic = "cqrswritetopic"
        #프로듀서 생성 
        pd = MessageProducer(broker, topic)
        #전송할 메시지 생성
        msg = {"task": "insert", "data": serializer.data}
        #메세지 전송
        res = pd.send_message(msg)
        print(res)
        #결과 반환
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

