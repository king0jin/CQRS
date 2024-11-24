#데이터 동기화를 위한 Kafka연결
import sys
import six
#Python 3.12 환경에서도 kafka-python 작동
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer
import threading
import json

from django.core.management import call_command
from django.apps import AppConfig
import pymysql
from pymongo import MongoClient
from datetime import datetime

#Kafka : 메세지전송 - MessageProducer클래스 생성
class MessageConsumer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.broker,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            group_id="jini", # Consumer group ID
            auto_offset_reset="earliest", # Start consuming from earliest available message
            enable_auto_commit=True, # Commit offsets automatically
        )
    #메세지를 수신하는 메서드 
    def receive_message(self):
        try:
            for message in self.consumer:
                result = json.loads(message.value)
                row = result["data"]
                doc = {'bid':row["bid"], 'title':row["title"],
                'author':row["author"], 'category':row["category"],
                'pages':row["pages"], 'price':row["price"],
                'published_date':row["published_date"],
                'description':row["description"]}
                #MongoDB에 연결
                conn = MongoClient('127.0.0.1')
                db = conn.cqrs
                collect = db.books
                #데이터 삽입
                collect.insert_one(doc)
                print("MongoDB 삽입 성공")
                #연결종료
                conn.close()
        except Exception as exc:
            raise exc

class ReadappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'readapp'
    #test : 앱을 시작하자마자 한 번만 읽기 작업 수행
    def ready(self):
        print("앱을 시작하였습니다.")
        #앱을 시작하자마자 MySQL데이터를 MongoDB로 복사하기
        print("MySQL에 데이터를 MongoDB로 복사하겠습니다.")
        #1. mysql 데이터베이스 연결
        con = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='000000',
                        db='cqrs',
                        charset ='utf8') 
           
        #2. Mongo DB 데이터베이스 연결
        conn = MongoClient('127.0.0.1', 27017)
        try:
            db_list = conn.list_database_names()  # MongoDB에 존재하는 데이터베이스 목록 가져오기
            print("연결 성공! 데이터베이스 목록:", db_list)
        except Exception as e:
            print("연결 실패:", e)
        #db 설정
        db = conn.cqrs
        #컬렉션 설정
        collect = db.books
        # 기존 컬렉션이 있으면 데이터 삭제 (필요 시 설정)
        try:
            if "books" in db.list_collection_names():
                print("기존 'books' 컬렉션이 존재합니다. 데이터를 초기화합니다.")
                collect.delete_many({})  # 기존 데이터 삭제
            else:
                print("'books' 컬렉션이 존재하지 않습니다. 새로 생성됩니다.")
        except Exception as e:
            print("컬렉션 확인 또는 초기화 중 오류 발생:", e)
            return
        
        #3. MySQL테이블 복사 준비
        #MySQL데이터 한 줄씩 읽어오기위한 cursor 생성
        cursor = con.cursor()
        
        #4. MySQL데이터 MongoDB에 복사
        #cursor로 MySQL데이터를 한 줄씩 읽어오는 쿼리 실행
        cursor.execute("select * from writeapp_book")
        #전체 데이터를 순회하며 가져와 튜플의 튜플로 생성하여 복사
        data = cursor.fetchall()
        for row in data:
            date = row[6].strftime("%Y-%m-%d")
            doc = {'bid':row[0], 'title':row[1],
                'author':row[2], 'category':row[3],
                'pages':row[4], 'price':row[5],
                'published_date':date, 'description':row[7]}
            collect.insert_one(doc)
        print("데이터 복사 완료")
        
        #5. MongoDB연결 종료
        con.close()

        #마이그레이션을 적용
        call_command('migrate')
        #메세지 수신자 
        broker = ["localhost:9092"]
        topic = "cqrswritetopic"
        consumer = MessageConsumer(broker, topic)
        #스레드로 메서드 호출
        t = threading.Thread(target=consumer.receive_message)
        print(t)
        t.start()
