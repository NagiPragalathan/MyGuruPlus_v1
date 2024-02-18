# Django  inbuilt models
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from QuizApp import settings

# Django views
from base.views.auth import *
from base.views.common import *
from base.views.FileManagement import *
from base.views.UserView import *
from base.views.QuestionManager import *
from base.views.Report import *
from base.views.Time_config import *
from base.views.Payment import *
from base.views.QuestionImport import *
from base.views.comment import *
from base.views.leaderboard import *
from base.views.LastUpdates import *
from base.views.Contect import *
from base.views.Error import *
from django.conf.urls import handler403, handler404, handler500

urlpatterns = []


handler404 = 'base.views.Error.custom_404'
handler500 = 'base.views.Error.custom_500'
handler403 = 'base.views.Error.custom_403'


admin_ = [
    path('admin/', admin.site.urls),    
]

auth = [
    path('accounts/', include('django.contrib.auth.urls')),  # Use built-in authentication views
    path('enter_otp', enter_otp, name='enter_otp'),
    path('signup/<str:mail>', signup, name='signup'),
    path('login', user_login, name='login'),
]

common = [
    path('home', home, name='home'),
    path('', home, name='home'),
    path('ad_home', home2, name='ad_home'),
    path('logout/', logout_view, name='logout'),
    path('contact_us', contact_us, name='contact_us'),
    path('test', test, name='test'),
    path('test1', test1, name='test1'),
]

file_manager = [
    path('add_data', add_data, name='add_data'),
    path('list_data', list_data, name='list_data'),
    path('add_folder', add_folder, name='add_folder'),
    path('list_folders/<str:path>', list_folders, name='list_folders'),
    path('edit_folder/<str:folder_id>/<str:path>', edit_folder, name='edit_folder'),
    path('delete_folder/<str:folder_id>/<str:path>', delete_folder, name='delete_folder'),
]

question_manager = [
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('add_question/<str:path>', add_question, name='add_question'),
    path('add_para_question/<str:path>', add_para_question, name='add_para_question'),
    path('edit_question/<str:path>', edit_question, name='edit_question'),
    path('para_edit_question/<str:path>/<str:cat>', para_edit_question, name='para_edit_question'),
    path('update_db', update_db, name='update_db'),
    path('add_image_editor', add_image_editor, name='add_image_editor'),
    path('update_para_db', update_para_db, name='update_para_db'),
    path('handle_questions', handle_questions, name='handle_questions'),
    path('handle_para_questions', handle_para_questions, name='handle_para_questions'),
    path('import_questions', import_questions, name='import_questions'),
    path('get_questions/<str:category>/', get_questions_by_category, name='get_questions_by_category'),
    path('delete_qust', delete_question, name='delete_question'),
    path('process_csv/<str:path>', process_csv, name='process_csv'),

    # Add other URL patterns if needed
]

UserView = [
    path('list_course/<str:path>', ListCourse, name='list_course'),
    path('view_course/<str:path>/<str:type>', free_courses, name='view_course'),
    path('take_quiz/<str:path>', take_quiz, name='take_quiz'),
    path('show_instructions/<str:path>', show_instructions, name='show_instructions'),
]

report = [
    path('create_report/<int:question_id>', create_report, name='create_report'),
    path('list_report', list_reports, name='list_reports'),
    path('update_report/<int:report_id>/', update_report, name='update_report'),
    path('delete_report/<int:report_id>/', delete_report, name='delete_report'),
]

time_config = [
    path('config_list/<str:path>', config_list, name='config_list'),
    path('create_config/<str:path>', create_config, name='create_config'),
    path('update_config/<int:config_id>/<str:path>', update_config, name='update_config'),
    path('delete_config/<int:config_id>/<str:path>', delete_config, name='delete_config'),
]

payments = [
     path('success/<str:path>' , success , name='success'),
     path('cost_course/<int:folder_id>' , cost_course , name='cost_course')
]

comment = [
     path('create_comment/<str:path>' , create_comment , name='create_comment'),
     path('update_rating/<str:path>' , update_rating , name='update_rating'),
     path('about_us',about_us,name="about_us"),
     path('disclaimer',disclaimer,name="disclaimer"),
     path('private_policy',private_policy,name="private_policy"),
     path('return_and_refund',return_and_refund,name="return_and_refund"),
     path('terms_and_condition',terms_and_condition,name="terms_and_condition"),
     
]

LeaderBoard_url = [
     path('update_leaderboard' , update_leaderboard , name='update_leaderboard'),
     path('leaderboard_view/<str:path>' , leaderboard_view , name='leaderboard_view'),
]

LastUpdates_url = [
     path('latest_update_list' , latest_update_list , name='latest_update_list'),
     path('create_latest_update' , create_latest_update , name='create_latest_update'),
     path('delete_latest_update/<int:pk>' , delete_latest_update , name='delete_latest_update'),
    
]

contact_url = [
     path('contacts_list', contact_list, name='contact_list'),
     path('submit_contact_form' , submit_contact_form , name='submit_contact_form'),
]
Error_url = [
     path('custom_404', custom_404, name='custom_404'),
     path('custom_500' , custom_500 , name='custom_500'),
     path('custom_403' , custom_403 , name='custom_403'),
]

urlpatterns.extend(admin_)
urlpatterns.extend(auth)
urlpatterns.extend(common)
urlpatterns.extend(file_manager)
urlpatterns.extend(question_manager)
urlpatterns.extend(UserView)
urlpatterns.extend(report)
urlpatterns.extend(time_config)
urlpatterns.extend(payments)
urlpatterns.extend(comment)
urlpatterns.extend(LeaderBoard_url)
urlpatterns.extend(LastUpdates_url)
urlpatterns.extend(contact_url)
urlpatterns.extend(Error_url)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
