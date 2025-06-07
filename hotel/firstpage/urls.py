from django.urls import path
from . import views

app_name = "firstpage"
urlpatterns = [
    path('',views.index,name="index"), 
    path('home/',views.index1,name="index1"),
    path('course/',views.course,name="course"),
    path('admission/',views.admn,name="admission"),
    path('fee/',views.fees,name="fee"),
    path('list/',views.lists,name="list"),

    path('fee_list/',views.feeList,name="feeList"),

    path('employee_corner/', views.employeeCorner, name='employeeCorner'),
    path('employee_attendance/', views.employeeAttendance, name='employeeAttendance'),


    # api
    path('get_student_by_roll_no', views.getStudentByRollNo, name='getStudentByRollNo'),
    path('get_receipt', views.getReceipt, name='getReceipt'),
    path('search_fee', views.searchFee, name='searchFee'),
    path('update_student', views.updateStudent, name='updateStudent'),
    path('delete_student', views.deleteStudent, name='deleteStudent'),
    path('search_student', views.searchStudent, name='searchStudent'),


    path('add_employee', views.addEmployee, name='addEmployee'),
    path('update_employee', views.updateEmployee, name='updateEmployee'),
    path('delete_employee', views.deleteEmployee, name='deleteEmployee'),
    path('search_employee', views.searchEmployee, name='searchEmployee'),

    path('getEmployeeAttendance', views.getEmployeeAttendance, name='getEmployeeAttendance'),

    path('update_employee_attendance', views.updateEmployeeAttendance, name='updateEmployeeAttendance'),
    path('delete_employee_attendance', views.deleteEmployeeAttendance, name='deleteEmployeeAttendance'),
    
    
    path('getReceiptHTML', views.getReceiptHTML, name='getReceiptHTML'),


    path('downloads/', views.downloads, name='downloads'),
    path('new_updates/', views.new_updates, name='new_updates'),


    path('add_new_update', views.add_new_update, name='add_new_update'),
    path('update_new_update', views.update_new_update, name='update_new_update'),
    path('delete_new_update', views.delete_new_update, name='delete_new_update'),


    path('logout/', views.logout_view, name='logout'),

    
]