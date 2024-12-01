# CQRS

## Server용 Application생성을 위한 가상 환경
### 가상화를 생성하고 활성화한다
+ 필요한 패키지를 설치한다 


**pip install django djangorestframework mysqlclient**


## 데이터 쓰기 작업 : write
### 1. 프로젝트와 애플리케이션 생성하기
**django-admin startproject 프로젝트이름 경로**


**python manage.py startapp 애플리케이션이름**

### 2. 프로젝트 설정 : settings.py
+ INSTALLED_APPS
  + 사용할 패키지와 애플리케이션 기재
+ DATABASE
  + 기본으로 sqlite3로 설정되어 있으므로 mysql로 변경
+ TIME_ZONE
  + Asia/Seoul로 변경
 
### 3. 요청 URL과 처리 함수
+ 요청 URL : urls.py
+ 처리함수 : views.py
+ 프로젝트 하나의 urls.py에 URL을 정의하면 관리하기 어려움으로 애플리케이션 별로 urls.py를 생성하여 해당 애플리케이션 관련 URL을 관리, 수정 할 수 있다.


### 실행
manage.py파일이 있는 디렉토리 위치에서 실행 명령 수행


**python manage.py runserver IP주소:포트번호**


+ 확인 : 브라우저로 확인


![image](https://github.com/user-attachments/assets/62856108-243d-40b9-947f-a77e9e5af57f)


### 4. 데이터 저장을 위한 모델(테이블)생성 : models.py
데이터베이스에 변경 사항이 있는 경우 데이터베이스 설정을 다시 해달라고 요청해야 적용이 된다.
1. python manage.py migrations 테이블이름
  + python manage.py makemigrations **writeapp**
2. python manage.py migrate
+ 내가 설정한 테이블이름으로 **테이블이름_모델명**으로 데이터베이스에 테이블이 생성된다
  + **writeapp_모델명**
#### 모델의 데이터를 JSON형식 문자열로 변환하여 출력해주는 Serializers(직렬화)생성


### 5. POST요청 
#### POST요청을 위한 URL작성 : urls.py
#### POST요청 처리 함수 생성 : views.py
서버를 실행하면 APIview화면을 볼 수 있다


![image](https://github.com/user-attachments/assets/f5b93caf-963d-4a5a-8220-f1af669446fa)
![image](https://github.com/user-attachments/assets/028b40f3-f801-4540-a78d-30b5391e102d)


+ content영역에 JSON형식으로 POST요청할 데이터를 작성하고 POST요청 버튼을 클릭


![image](https://github.com/user-attachments/assets/3103de84-44f4-4c29-9fba-42433924c95f)


+ APIview로 POST요청 응답메세지를 확인
+ POST요청이 성공적으로 완료되면 데이터베이스에서도 삽입이 되었는지 확인


![image](https://github.com/user-attachments/assets/031f1510-3df3-46bb-a9e4-fc5a5b20c4b6)


+ 내가 POST요청한 데이터가 성공적으로 데이터베이스에 삽입 되었다 
---
## Client Apllication
#### 1. react Project 생성 : **yarn create react-app cqrsclient**
#### 2. react Application 실행 : **yarn start**
#### 3. React 프로젝트에서 아이콘 사용을 위한 패키지 설치
  + **npm install --save --legacy-peer-deps @material-ui/core**
  + **npm install --save --legacy-peer-deps @material-ui/icons**
#### 4. 비동기 데이터 요청을 쉽게 작성하기 위한 패키지 설치
  + **yarn add axios**

### 사용자가 데이터 삽입 수행하기 위한 컴포넌트 생성 : src/AddBook.jsx
+ 기능을 독립적으로 관리하기 위해 기능별로 jsx파일을 생성
### AddBook.jsx컴포넌트를 화면에 출력 : App.js
+ import로 jsx파일들을 연결하여 jsx파일에 생성한 컴포넌트를 HTML형식으로 화면에 렌더링한다


#### 5. server(Django-write)와 client(react)실행
![image](https://github.com/user-attachments/assets/64d7fb9e-d3b2-4ac1-8ac7-26be5c1dbe65)
![image](https://github.com/user-attachments/assets/c6f4979a-3933-4f63-ad55-a0b0c55f5855)


+ 화면으로 데이터를 삽입하려고하면 CORS에러가 발생한다
  + 기본적으로 웹 브라우저는 보안을 위해 동일 출처 정책(Same-Origin Policy)을 적용하기 때문이다
  + 서버 : 헤더에 어떤 출처가 요청을 할 수 있는지 허용할지를 명시가 가능하다
### CORS에러 해결 : write 디렉토리
1. 가상환경으로 전환하여 **django-cors-headers**패키지 설치
2. settings.py 수정
   + INSTALLES_APPS : corsheaders 추가
   + MIDDLEWARE 제일 상단 : corsheaders.middleware.CorsMiddleware 추가
   + 빈 곳에 CORS_ORIGIN_WHITELIST = ['허용할 URL',,,] 추가
   + 빈 곳에 CORS_ALLOW_CREDENTIALS = True 추가
3. server만 재실행하여 화면에서 삽입 수행


![image](https://github.com/user-attachments/assets/ed6ebc00-3471-4f3a-9af5-2547dac2b4cd)


+ 데이터베이스에 삽입이 되었는지 확인


![image](https://github.com/user-attachments/assets/731d1d71-bd34-4bf7-8f74-eca13fb195fa)

---
## Client용 Application생성을 위한 가상 환경
Application을 시작할 때 관계형 데이터베이스의 모든 데이터를 복사하여 MongoDB로 저장하고 클라이언트 요펑이 오면 MongoDB데이터베이스로 부터 데이터를 전달받는다
### 가상화를 생성하고 활성화한다
+ 필요한 패키지를 설치한다 


**pip install django djangorestframework mysql django-cors-headers pymongo**

## 데이터 읽기 작업 : read
### 1. 프로젝트와 애플리케이션 생성하기
**django-admin startproject 프로젝트이름 경로**


**python manage.py startapp 애플리케이션이름**

### 2. 프로젝트 설정 : settings.py
+ INSTALLED_APPS
  + 사용할 패키지와 애플리케이션 기재
+  MIDDLEWARE
  + MIDDLEWARE 제일 상단 : corsheaders.middleware.CorsMiddleware 추가
+ 빈 곳에 CORS_ORIGIN_WHITELIST = ['허용할 URL',,,] 추가
+ 빈 곳에 CORS_ALLOW_CREDENTIALS = True 추가

### 3. Apllicaiton을 수행할 때 딱 한 번만 읽기 작업 수행 : apps.py - ReadappConfig클래스 : read()
+ settings.py : INSTALLED_APPS 추가 설정
  + **readapp.apps.ReadappConfig**

### 실행
manage.py파일이 있는 디렉토리 위치에서 실행 명령 수행


**python manage.py runserver IP주소:포트번호**
+ 위 실행 명령을 수행하면 consol로 read()의 내용이 실행되었는지 확인할 수 있다 


![image](https://github.com/user-attachments/assets/3e694172-9e50-4e5d-bf1f-eae93668237c)

+ server 연결 확인 : 브라우저로 확인


![image](https://github.com/user-attachments/assets/a8c8ec5b-f903-4b96-9654-515898f70e27)


### 4. Application을 시작할 때 관계형 데이터베이스의 모든 데이터를 복사하여 MongoDB로 저장 : apps.py
### read()에 sync_mysql_to_mongo()포함
#### sync_mysql_to_mongo() 생성
1. 관계형 데이터베이스 연결
2. MongoDB 데이터베이스 연결
3. MongoDB 데이터베이스, 컬렉션 설정
4. 관겨형 데이터베이스 데이터 복사 준비
5. 관겨형 데이터베이스 데이터 복사하여 튜블로 생성
6. 튜플로 복사한 데이터 MongoDB데이터베이스 컬렉션에 복사
7. 연결 종료

### 실행
manage.py파일이 있는 디렉토리 위치에서 실행 명령 수행하고 MongoDB Compass로 확인


![image](https://github.com/user-attachments/assets/d81186d8-a124-476c-9a97-3640bde6af2c)


### 5. 요청 URL과 처리 함수
+ 요청 URL : urls.py
+ 처리함수 : views.py
  + MongoDB데이터베이스로 부터 데이터를 전달받기 위하여 **MongoDB데이터베이스 연결, 데이터베이스 설정, 컬렉션 설정**

### 실행
manage.py파일이 있는 디렉토리 위치에서 실행 명령 수행


**python manage.py runserver IP주소:포트번호**


![image](https://github.com/user-attachments/assets/732aeacc-3e00-4976-91cd-8a0ad7fbdd34)


+ MongoDB데이터베이스에 저장되어 있는 데이터를 전달 받아 APIview로 확인 
---
## Client Apllication 수정
1. 화면이 렌더링된 이후에 바로 수행될 함수 추가 : useEffect()
2. 데이터베이스를 읽어서 화면에 title, page, price 출력 
### 실행
manage.py파일이 있는 디렉토리 위치에서 실행 명령 수행
+ write : **python manage.py runserver 127.0.0.1:8080**
+ read : **python manage.py runserver 127.0.0.1:7000**
+ client : **yarn start**


![스크린샷 2024-11-24 123708](https://github.com/user-attachments/assets/48dec320-69c5-4045-b539-2c6e8582eac9)

#### 데이터 삽입 수행
![스크린샷 2024-11-24 123812](https://github.com/user-attachments/assets/0e3b126f-794e-445d-b943-e7f9f96f3dc8)
![스크린샷 2024-11-24 123826](https://github.com/user-attachments/assets/6baf1264-006b-46bf-ac9d-aca900f9429e)


+ 쓰기전용 데이터베이스에 삽입이 되었는지 확인
![스크린샷 2024-11-24 123846](https://github.com/user-attachments/assets/35853e33-195d-42ed-95ab-e72f88684095)

+ 읽기전용 데이터베이스에도 데이터가 복사되었는지 확인
![image](https://github.com/user-attachments/assets/796ac5f2-ddee-4212-9ec1-7170531ffe88)
  + 복사가 되지 않았다
  + 화면을 새로 고침하여도 새로 추가된 데이터는 화면에 title이 출력됮 않는다 
![스크린샷 2024-11-24 123708](https://github.com/user-attachments/assets/99436340-4e05-40a5-9286-6009413ce3d0)


**서버를 데이터 사용 용도에 따라 분리 시켜서 구현하고 저장소도 분리를 시켜 구현하는 것을 Polyglot하다고 할 수 있다**
+ **CQRS로 구현한 것은 맞으나 데이터 동기화가 이루어 지지 않은 상태이다**
---
## write 프로젝트 Kafka연결
데이터 삽입할 때 Kafka로 topic을 전달하도록 수정 : views.py
1. write 디렉토리 가상환경 활성화하여 패키지 설치
   + **pip install kafka-python**
2. Python 3.12 환경에서도 kafka-python이 작동할 수 있도록 설정
3. MessageProducer클래스 생성 : send_message()
  
## read 프로젝트 Kafka연결
데이터 출력할 때 Kafka의 topic을 수신하도록 수정 : apps.py
+ topic을 수신하는 쪽은 백그라운드에서 계속 대기중이어야한다
  + 비동기적으로 백그라운드에서 계속 수행 중이어야 한다
1. read 디렉토리 가상환경 활성화하여 패키지 설치
   + **pip install kafka-python**
2. Python 3.12 환경에서도 kafka-python이 작동할 수 있도록 설정
3. MessageConsumer클래스 생성 : receive_message()

## client 프로젝트 Kafka연결
+ 사용자가 데이터 삽입을 수행하면 새로 추가된 데이터를 자동으로 화면에 출력하도록 설정 : App.js
1. const [items, setItems] = useState([]); : 상태를 생성하여 사용자가 데이터 삽입을 할 시 상태변화를 줌으로써 상태 변화를 감지하여 데이터를 다시 불러오도록 수정
2. useEffect 훅 : 컴포넌트가 처음 렌더링될 때 한 번만 실행
   + [] 빈 배열을 의존성 배열로 전달하면 첫 렌더링 후에만 실행
3. Axios.get() : 서버에서 책 목록을 불러옴 
4. Axios.post() : 새로운 책 데이터를 서버에 추가
   + 서버에서 응답으로 bid가 있으면 setItems()를 사용해 items 배열에 새 책 데이터를 추가하여 화면에 반영
6. PostBook 컴포넌트를 렌더링 : post 함수(책 추가 함수)를 props로 전달
