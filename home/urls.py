from django.contrib.auth import views as auth_views
from django.urls import path
from home import views

urlpatterns = [
    path('', views.login_form, name='login_form'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('register/', views.register.as_view(), name='register'),
    path('student/', views.student, name='student'),
    path('update/', views.update, name='update'),
    path('password/', views.password, name='password'),
    path('logout_student/', views.logout_student, name='logout_student'),
    path('loading_page/', views.loading_page, name='loading_page'),
    path('ready_to_test/<str:code>/', views.ready_to_test, name='ready_to_test'),
    path('post_exam_two/<int:id>/', views.post_exam_two, name='post_exam_two'),
    path('course_detail/<str:code>/', views.course_detail, name='course_detail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Authenticate/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='Authenticate/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Authenticate/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Authenticate/password_reset_complete.html'), name='password_reset_complete'),
]