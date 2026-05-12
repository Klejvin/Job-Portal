from django.urls import path
from.import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path("",views.home,name="homePage"),
    path("pune/",views.pune,name="punePage"),
    path("rrethnesh/",views.rrethnesh,name="aboutPage"),
    path("pyetje/",views.pyetje,name="pyetjePage"),
    path("partneret/",views.partneret,name="partneretPage"),
    path('behu_partner/', views.behu_partner, name='behupartnerPage'),
    path('pune/<int:pk>/', views.job_detail, name='detailsPage'),
    path("login/",views.loginPage,name="loginPage"),
    path("register/",views.register,name="registerPage"),
    path("logout/", auth_views.LogoutView.as_view(next_page='homePage'), name="logout"),
    path('add_job/', views.add_job_custom, name='add_job_custom'),
    path('edit_job/<int:pk>/', views.edit_job, name='edit_job'),
    
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('delete_job/<int:pk>/', views.delete_job, name='delete_job'),
    path('aplikim/<int:pk>/', views.aplikim, name='aplikimPage'),
    path('cv/', views.cv_view, name='cvPage'),
    path('aplikimet_e_mia/', views.aplikimet_e_mia, name='my_applicationsPage'),
    # 1. Faqja për të kërkuar reset
    path('reset_password/', views.custom_password_reset, name="password_reset"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
    



]
