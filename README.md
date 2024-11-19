# CQRS

## Server용 Application생성을 위한 가상 환경
### 가상화를 생성하고 활성화한다
+ 필요한 패키지를 설치한다 


**pip install django djangorestframework mysqlclient**


## 데이터 쓰기 작업 : write
1. 프로젝트와 애플리케이션 생성하기
**django-admin startproject 프로젝트이름 경로**


**python manage.py startapp 애플리케이션이름**

2. 프로젝트 설정 : settings.py
+ INSTALLED_APPS
  + 사용할 패키지와 애플리케이션 기재
+ DATABASE
  + 기본으로 sqlite3로 설정되어 있으므로 mysql로 변경
+ TIME_ZONE
  + Asia/Seoul로 변경
 
3. 요청 URL과 처리 함수
+ 요청 URL : urls.py
+ 처리함수 : views.py
+ 프로젝트 하나의 urls.py에 URL을 정의하면 관리하기 어려움으로 애플리케이션 별로 urls.py를 생성하여 해당 애플리케이션 관련 URL을 관리, 수정 할 수 있다.


### 실행
manage.py파일이 있는 디렉토리 위치에서 실행 명령 수행


**python manage.py runserver IP주소:포트번호**


+ 확인 : 브라우저로 확인


![image](https://github.com/user-attachments/assets/62856108-243d-40b9-947f-a77e9e5af57f)

---
## 데이터 읽기 작업 : read
