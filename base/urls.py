from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import home,auth,classs,assignments,submissions

urlpatterns = [
    path('',home.landing_page,name='landing_page'),
    path('login/',auth.login_view,name='login'),
    path('register/',auth.register_view,name='register'),
    path('logout/', auth.logout_view,name='logout'),
    path('home/',home.home,name='home'),
    path('class/<int:id>',classs.render_class,name='render_class'),
    path('create_assignment/<int:classroom_id>',assignments.create_assignment,name='create_assignment'),
    path('assignment_summary/<int:assignment_id>',assignments.assignment_summary,name='assignment_summary'),
    path('delete_assignment/<int:assignment_id>',assignments.delete_assignment,name='delete_assignment'),
    path('unenroll_class/<int:classroom_id>',classs.unenroll_class,name='unenroll_class'),
    path('delete_class/<int:classroom_id>',classs.delete_class,name='delete_class'),
    path('create_class_request/',classs.create_class_request,name='create_class_request'),
    path('join_class_request/',classs.join_class_request,name='join_class_request'),
    path('submit_assignment_request/<int:assignment_id>',submissions.submit_assignment_request,name='submit_assignment_request'),
    path('mark_submission_request/<int:submission_id>/<int:teacher_id>',submissions.mark_submission_request,name='mark_submission_request')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)