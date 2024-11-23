from django.apps import AppConfig


class ReadappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'readapp'
    #test : 앱을 시작하자마자 한 번만 읽기 작업 수행
    def ready(self):
        print("앱을 시작하였습니다.")
