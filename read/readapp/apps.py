import pymysql
from pymongo import MongoClient
from datetime import datetime

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

#Kafka : 메세지수신 - MessageProducer클래스 생성
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
            print("Kafka Consumer 시작...")
            for message in self.consumer:
                try:
                    result = json.loads(message.value)
                    row = result["data"]
                    doc = {
                        'bid':row["bid"], 'title':row["title"],
                        'author':row["author"], 'category':row["category"],
                        'pages':row["pages"], 'price':row["price"],
                        'published_date':row["published_date"],
                        'description':row["description"]
                    }
                    #MongoDB에 연결
                    with MongoClient('127.0.0.1', 27017) as conn:
                        db = conn.cqrs
                        collect = db.books
                        #데이터 삽입
                        collect.insert_one(doc)
                        print("MongoDB 삽입 성공")
                except Exception as exc:
                    print("메시지 처리 중 오류 발생:", exc)
        except Exception as exc:
            print("Kafka Consumer 오류 발생:", exc)

class ReadappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'readapp'
    #test : 앱을 시작하자마자 한 번만 읽기 작업 수행
    def ready(self):
        print("앱을 시작하였습니다.")
        #메세지 수신자 
        broker = ["localhost:9092"]
        topic = "cqrswritetopic"
        consumer = MessageConsumer(broker, topic)
        #스레드로 메서드 호출
        consumer_thread = threading.Thread(target=consumer.receive_message, daemon=True)
        consumer_thread.start()
        print("Kafka Consumer 스레드가 시작되었습니다.")

        #앱을 시작하자마자 MySQL데이터를 MongoDB로 복사하기
        print("MySQL에 데이터를 MongoDB로 복사하겠습니다.")
        self.sync_mysql_to_mongo()

    def sync_mysql_to_mongo(self):
        try:
            # MySQL 연결
            con = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                user="root",
                passwd="000000",
                db="cqrs",
                charset="utf8",
            )
            cursor = con.cursor()

            # MongoDB 연결
            with MongoClient("127.0.0.1", 27017) as conn:
                db = conn.cqrs
                collect = db.books
                # 기존 데이터 초기화
                collect.delete_many({})
                print("기존 MongoDB 데이터 초기화 완료.")

                # MySQL 데이터 복사
                cursor.execute("SELECT * FROM writeapp_book")
                data = cursor.fetchall()
                for row in data:
                    date = row[6].strftime("%Y-%m-%d")
                    doc = {
                        "bid": row[0],
                        "title": row[1],
                        "author": row[2],
                        "category": row[3],
                        "pages": row[4],
                        "price": row[5],
                        "published_date": date,
                        "description": row[7],
                    }
                    collect.insert_one(doc)
                print("MySQL 데이터 MongoDB 복사 완료.")
            con.close()
        except Exception as e:
            print("MySQL -> MongoDB 복사 중 오류 발생:", e)