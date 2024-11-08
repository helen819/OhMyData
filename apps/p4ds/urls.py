from django.urls import path
from . import views

app_name = "p4ds"

urlpatterns = [
    path("", views.index, name="index"),
    # 추후 app을 나눠주면 해당되는 폴더 내로 url과 view를 이동할 예정
    path("api/user/register/", views.user_register, name="user_register"),
    path("api/user/login/", views.user_login, name="user_login"),
    path("api/user/logout/", views.user_logout, name="user_logout"),
    path("api/analytics/report/", views.analytics_report, name="analytics_report"),
    path("api/practice/set/", views.practice_set, name="practice_set"),
    path("api/practice/complete/", views.practice_complete, name="practice_complete"),
]