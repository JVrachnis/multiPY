"""multyPY URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from django.conf import settings

from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('', views.home,name='home'),
    path('students/', views.students,name='students'),
    path('profile/<str:username>',views.view_profile,name='profile'),
    path('profile',views.ac_profile,name='ac_profile'),
    path('edit_permitions/<str:username>',views.edit_permitions,name='edit_permitions'),
    path('keycodes',views.keycodes,name='keycodes'),
    path('signup/',views.register,name='signup'),
    path('register/',views.register,name='register'),
    path('study_material_pdf', TemplateView.as_view(template_name='study_material_pdf.html'),name='study_material_pdf'),
    path('multiplication_tables', views.multiplication_tables,name='multiplication_tables'),
    path('multiplication_table/<int:base_number>', views.multiplication_table,name='multiplication_table'),
    path('multiplication_table_ex/<int:base_number>/', views.exam,name='multiplication_table_ex'),
    path('multiple_choice', views.multiple_choice_tr,name='multiple_choice'),
    path('multiple_choice/<int:base_number>', views.multiple_choice_r,name='multiple_choice'),
    path('multiple_choice/<int:base_number>/<int:multiplier>/', views.multiple_choice,name='multiple_choice'),
    path('multiplication_tables_ex', views.exams,name='multiplication_tables_ex'),
    path('answers', views.answers, name='answers'),
    path('answers/<str:username>', views.view_answers, name='answers'),
    path('exam_answers/<str:username>', views.view_exam_answers, name='exam_answers'),
    path('final_exam_answers/<str:username>', views.view_final_exam_answers, name='final_exam_answers'),
    path('json/progress/exercises',views.json_test,name='json_progress_exercises'),
    path('json/progress/top_exam',views.json_progress_top_exam,name='json_progress_top_exam'),
    path('json/progress/total_exam',views.json_progress_total_exam,name='json_progress_total_exam'),
    path('help/<int:helppage>',views.helppage,name='help')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
