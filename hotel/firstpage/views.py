from django.shortcuts import render, redirect
from django.urls import reverse

from datetime import datetime
from .models import Student, Fee, Employee, EmployeeAttendance, NewUpdate

from django.http import JsonResponse
from .serializers import StudentSerializer, FeeSerializer, EmployeeSerializer, EmployeeAttendanceSerializer, NewUpdateSerializer

from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
import json

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from django.conf import settings

import inflect

import os

from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout, authenticate


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('home:index1'))
    if request.method=='POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(reverse('firstpage:index1'))

    my_template="login.html"
    return render(request,my_template)

@login_required
def index1(request):
    my_template="home.html"
    return render(request,my_template)

@login_required
def course(request):
    my_template = "courses.html"
    return render(request,my_template)

@login_required
def admn(request):
    if request.method=='POST':
        dob = request.POST['dob']

        class10_details = {
            "board": request.POST['board_x'],
            "percentage": request.POST['percentage_x'],
            "year_of_passing": request.POST['year_x']
        }
        class12_details = {
            "board": request.POST['board_xii'],
            "percentage": request.POST['percentage_xii'],
            "year_of_passing": request.POST['year_xii']
        }
        graduation_details = {
            "board": request.POST['board_graduation'],
            "percentage": request.POST['percentage_graduation'],
            "year_of_passing": request.POST['year_graduation']
        }
        masters_details = {
            "board": request.POST['board_masters'],
            "percentage": request.POST['percentage_masters'],
            "year_of_passing": request.POST['year_masters']
        }

        courses_applied = request.POST.getlist('courses')

        if len(request.FILES)>0:
            student = Student(fullname=request.POST['full_name'], dob=dob, email=request.POST['email'], mobile_number=request.POST['mobile'], gender=request.POST['gender'], address=request.POST['address'], fathername=request.POST['father_name'], class10_details=class10_details, class12_details=class12_details, graduation_details=graduation_details, masters_details=masters_details, pfp=request.FILES['photo'], courses_applied=courses_applied)
            student.save()

        else:
            student = Student(fullname=request.POST['full_name'], dob=dob, email=request.POST['email'], mobile_number=request.POST['mobile'], gender=request.POST['gender'], address=request.POST['address'], fathername=request.POST['father_name'], class10_details=class10_details, class12_details=class12_details, graduation_details=graduation_details, masters_details=masters_details, courses_applied=courses_applied)
            student.save()
        
    my_template = "admission.html"
    return render(request,my_template)

@login_required
def fees(request):
    if request.method == 'POST':
        student = Student.objects.get(rollnumber=request.POST['roll_number'])

        receipt_number = 1600
        if Fee.objects.count()>0:
            receipt_number = Fee.objects.last().receipt_number + 1

        fee = Fee(student=student, receipt_number=receipt_number, fee_amount=request.POST['fee_amount'], deposit_date=request.POST['deposit_date'])
        fee.save()

    my_template = "Fee.html"
    return render(request,my_template)

@login_required
def lists(request):
    students = Student.objects.all().order_by('-enrollment_date').prefetch_related('fee')
    serializer = StudentSerializer(students, many=True)

    serialized_json = json.dumps(serializer.data, cls=DjangoJSONEncoder)
    

    my_template = "list_of_all_st.html"
    context = {
        'students': serialized_json
    }
    return render(request,my_template, context)

@login_required
def feeList(request):
    fee_list = Fee.objects.all().order_by('-deposit_date')
    serializer = FeeSerializer(fee_list, many=True)

    serialized_json = json.dumps(serializer.data, cls=DjangoJSONEncoder)


    my_template = "fee_detail_list.html"
    context = {
        'fee_list': serialized_json,
    }
    return render(request,my_template, context)


@login_required
def getStudentByRollNo(request):
    if request.method == 'GET':
        rollNo = request.GET['rollNo']
        student = Student.objects.get(rollnumber=rollNo)

        data = {
            'name': student.fullname,
            'fathername': student.fathername,
            'address': student.address,
            'pfp': student.pfp.url if student.pfp else None,
            'courses_applied': student.courses_applied
        }

        return JsonResponse(data)


def get_image_base64(image_path):
    with default_storage.open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@login_required
def getReceipt(request):
    # return render(request, 'receipt.html')
    fee = Fee.objects.get(receipt_number=request.GET['receipt_number'])

    static_url = settings.STATIC_URL

    p = inflect.engine()

    this_folder = os.path.dirname(os.path.abspath(__file__))

    signature_path = 'file://' + os.path.join(this_folder, 'static', 'signature.jpg' )
    logo_path = 'file://' + os.path.join(this_folder, 'static', 'logo.png' )


    context = {
        'receipt_number': fee.receipt_number,
        'date': fee.deposit_date,
        'fees_amount_in_words': p.number_to_words(fee.fee_amount).capitalize() + ' only',
        'student_name': fee.student.fullname,
        'father_name': fee.student.fathername,
        'address': fee.student.address,
        'fees_amount': fee.fee_amount,
        'signature': signature_path,
        'logo': logo_path
    }


    html_string = render_to_string('receipt.html', context)
    pdf_file = HTML(string=html_string).write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="document.pdf"'
    return response



@login_required
def getReceiptHTML(request):
    # return render(request, 'receipt.html')
    fee = Fee.objects.get(receipt_number=request.GET['receipt_number'])


    p = inflect.engine()


    context = {
        'receipt_number': fee.receipt_number,
        'date': fee.deposit_date,
        'fees_amount_in_words': p.number_to_words(fee.fee_amount).capitalize() + ' only',
        'student_name': fee.student.fullname,
        'father_name': fee.student.fathername,
        'address': fee.student.address,
        'fees_amount': fee.fee_amount,
    }


    html_string = render_to_string('receipt.html', context)
    
    response = HttpResponse(html_string)
    return response



@login_required
def updateStudent(request):
    if request.method=='POST':
        dob = request.POST['dob']

        class10_details = {
            "board": request.POST['board_x'],
            "percentage": request.POST['percentage_x'],
            "year_of_passing": request.POST['year_x']
        }
        class12_details = {
            "board": request.POST['board_xii'],
            "percentage": request.POST['percentage_xii'],
            "year_of_passing": request.POST['year_xii']
        }
        graduation_details = {
            "board": request.POST['board_graduation'],
            "percentage": request.POST['percentage_graduation'],
            "year_of_passing": request.POST['year_graduation']
        }
        masters_details = {
            "board": request.POST['board_masters'],
            "percentage": request.POST['percentage_masters'],
            "year_of_passing": request.POST['year_masters']
        }

        courses_applied = request.POST.getlist('courses')

        
        student = Student.objects.get(rollnumber=request.POST['roll_number'])
        student.fullname=request.POST['full_name']
        student.dob=dob
        student.email=request.POST['email']
        student.mobile_number=request.POST['mobile']
        student.gender=request.POST['gender']
        student.address=request.POST['address']
        student.fathername=request.POST['father_name']
        student.class10_details=class10_details
        student.class12_details=class12_details
        student.graduation_details=graduation_details
        student.masters_details=masters_details
        student.courses_applied=courses_applied
        if len(request.FILES)>0:
            pfp = request.FILES['photo']
            if pfp is not None:
                student.pfp = pfp

        student.save()

        return redirect(reverse('firstpage:list'))
    return JsonResponse({'message': 'Use post request'})


@login_required
def deleteStudent(request):
    if request.method=='POST':
        student = Student.objects.get(rollnumber=request.POST['roll_number'])
        student.delete()
        return redirect(reverse('firstpage:list'))
    return JsonResponse({'message': 'Use post request'})


@login_required
def searchFee(request):
    query = request.GET.get('q', '')
    results = []


    if query=='':
        print('n')
        students = Student.objects.all()

        # Get the rollnumbers of the filtered students
        student_rollnumbers = students.values_list('rollnumber', flat=True)
        
        # Filter fees based on the filtered students
        fees = Fee.objects.filter(student__rollnumber__in=student_rollnumbers)
        
        # Prepare data to return
        results = []
        for fee in fees:
            student = fee.student
            results.append({
                'rollnumber': student.rollnumber,
                'receipt_number': fee.receipt_number,
                'fullname': student.fullname,
                'email': student.email,
                'deposit_date': fee.deposit_date,
                'fee_amount': fee.fee_amount,
                'pfp_url': student.pfp.url if student.pfp else None
            })
            
        return JsonResponse(results, safe=False)
    
    else:
        students = Student.objects.filter(fullname__icontains=query)

        # Get the rollnumbers of the filtered students
        student_rollnumbers = students.values_list('rollnumber', flat=True)
        
        # Filter fees based on the filtered students
        fees = Fee.objects.filter(student__rollnumber__in=student_rollnumbers)
        
        # Prepare data to return
        results = []
        for fee in fees:
            student = fee.student
            results.append({
                'rollnumber': student.rollnumber,
                'receipt_number': fee.receipt_number,
                'fullname': student.fullname,
                'email': student.email,
                'deposit_date': fee.deposit_date,
                'fee_amount': fee.fee_amount,
                'pfp_url': student.pfp.url if student.pfp else None
            })
            
        return JsonResponse(results, safe=False)


@login_required 
def searchStudent(request):
    query = request.GET.get('q', '')
    results = []


    if query=='':
        print('n')
        students = Student.objects.all()

        
        # Prepare data to return
        results = []
        for student in students:
            results.append({
                'rollnumber': student.rollnumber,
                'fullname': student.fullname,
                'email': student.email,
                'mobile_number': student.mobile_number,
                'pfp': student.pfp.url if student.pfp else None
            })
            
        return JsonResponse(results, safe=False)
    
    else:
        students = Student.objects.filter(fullname__icontains=query)

        
        # Prepare data to return
        results = []
        for student in students:
            results.append({
                'rollnumber': student.rollnumber,
                'fullname': student.fullname,
                'email': student.email,
                'mobile_number': student.mobile_number,
                'pfp': student.pfp.url if student.pfp else None
            })
            
        return JsonResponse(results, safe=False)

   



@login_required
def employeeCorner(request):
    employees = Employee.objects.all().order_by('-joining_date')
    serializer = EmployeeSerializer(employees, many=True)

    serialized_json = json.dumps(serializer.data, cls=DjangoJSONEncoder)


    my_template = "employee_corner.html"
    context = {
        'employees': serialized_json
    }
    return render(request,my_template, context)


@login_required
def addEmployee(request):
    if request.method=='POST':
        dob = request.POST['dob']
        joining_date = request.POST['joining_date']

        class10_details = {
            "board": request.POST['board_x'],
            "percentage": request.POST['percentage_x'],
            "year_of_passing": request.POST['year_x']
        }
        class12_details = {
            "board": request.POST['board_xii'],
            "percentage": request.POST['percentage_xii'],
            "year_of_passing": request.POST['year_xii']
        }
        graduation_details = {
            "board": request.POST['board_graduation'],
            "percentage": request.POST['percentage_graduation'],
            "year_of_passing": request.POST['year_graduation']
        }
        masters_details = {
            "board": request.POST['board_masters'],
            "percentage": request.POST['percentage_masters'],
            "year_of_passing": request.POST['year_masters']
        }


        if len(request.FILES)>0:
            employee = Employee(fullname=request.POST['full_name'], dob=dob, email=request.POST['email'], mobile_number=request.POST['mobile'], gender=request.POST['gender'], address=request.POST['address'], joining_date=joining_date, class10_details=class10_details, class12_details=class12_details, graduation_details=graduation_details, masters_details=masters_details, pfp=request.FILES['photo'])
            employee.save()

        else:
            employee = Employee(fullname=request.POST['full_name'], dob=dob, email=request.POST['email'], mobile_number=request.POST['mobile'], gender=request.POST['gender'], address=request.POST['address'], joining_date=joining_date, class10_details=class10_details, class12_details=class12_details, graduation_details=graduation_details, masters_details=masters_details)
            employee.save()
        
    return redirect(reverse('firstpage:employeeCorner'))


@login_required
def updateEmployee(request):
    if request.method=='POST':
        dob = request.POST['dob']
        joining_date = request.POST['joining_date']

        class10_details = {
            "board": request.POST['board_x'],
            "percentage": request.POST['percentage_x'],
            "year_of_passing": request.POST['year_x']
        }
        class12_details = {
            "board": request.POST['board_xii'],
            "percentage": request.POST['percentage_xii'],
            "year_of_passing": request.POST['year_xii']
        }
        graduation_details = {
            "board": request.POST['board_graduation'],
            "percentage": request.POST['percentage_graduation'],
            "year_of_passing": request.POST['year_graduation']
        }
        masters_details = {
            "board": request.POST['board_masters'],
            "percentage": request.POST['percentage_masters'],
            "year_of_passing": request.POST['year_masters']
        }


        
        employee = Employee.objects.get(id=request.POST['id'])

        employee.fullname=request.POST['full_name']
        employee.dob=dob
        employee.email=request.POST['email']
        employee.mobile_number=request.POST['mobile']
        employee.gender=request.POST['gender']
        employee.address=request.POST['address']
        employee.joining_date=request.POST['joining_date']
        employee.class10_details=class10_details
        employee.class12_details=class12_details
        employee.graduation_details=graduation_details
        employee.masters_details=masters_details
        if len(request.FILES)>0:
            pfp = request.FILES['photo']
            if pfp is not None:
                employee.pfp = pfp

        employee.save()

        return redirect(reverse('firstpage:employeeCorner'))
    return JsonResponse({'message': 'Use post request'})


@login_required
def deleteEmployee(request):
    if request.method=='POST':
        employee = Employee.objects.get(id=request.POST['id'])
        employee.delete()
        return redirect(reverse('firstpage:employeeCorner'))
    return JsonResponse({'message': 'Use post request'})


@login_required
def searchEmployee(request):
    query = request.GET.get('q', '')
    results = []


    if query=='':
        print('n')
        employees = Employee.objects.all()

        
        # Prepare data to return
        results = []
        for employee in employees:
            results.append({
                'id': employee.id,
                'fullname': employee.fullname,
                'email': employee.email,
                'mobile_number': employee.mobile_number,
                'pfp': employee.pfp.url if employee.pfp else None
            })
            
        return JsonResponse(results, safe=False)
    
    else:
        employees = Employee.objects.filter(fullname__icontains=query)

        
        # Prepare data to return
        results = []
        for employee in employees:
            results.append({
                'id': employee.id,
                'fullname': employee.fullname,
                'email': employee.email,
                'mobile_number': employee.mobile_number,
                'pfp': employee.pfp.url if employee.pfp else None
            })
            
        return JsonResponse(results, safe=False)


@login_required
def employeeAttendance(request):
    if request.method=='POST':
        employee = Employee(id=request.POST['employee'])
        attendance = EmployeeAttendance(employee=employee, date=request.POST['date'], status=request.POST['status'], remarks=request.POST['remarks'])
        attendance.save()

    
    employees = Employee.objects.all().values('id', 'fullname', 'pfp')

    context = {
        'employees': employees
    }

    my_template = 'employee_attendance.html'
    return render(request, my_template, context=context)


@login_required
def getEmployeeAttendance(request):
        id = request.GET.get('id', '')

        employee = Employee.objects.get(id=id)
        employee_attendance = EmployeeAttendance.objects.filter(employee=employee)

        serializer = EmployeeAttendanceSerializer(employee_attendance, many=True)

        results = json.dumps(serializer.data, cls=DjangoJSONEncoder)
            
        return JsonResponse(results, safe=False)


@login_required   
def updateEmployeeAttendance(request):
    if request.method=='POST':
        
        employee = Employee.objects.get(id=request.POST['id'])
        attendance = EmployeeAttendance.objects.get(employee=employee)

        attendance.date=request.POST['date']
        attendance.status=request.POST['status']
        attendance.remarks=request.POST['remarks']

        attendance.save()

        return redirect(reverse('firstpage:employeeAttendance'))
    return JsonResponse({'message': 'Use post request'})


@login_required
def deleteEmployeeAttendance(request):
    if request.method=='POST':
        attendance = EmployeeAttendance.objects.get(id=request.POST['id'])
        attendance.delete()
        return redirect(reverse('firstpage:employeeAttendance'))
    return JsonResponse({'message': 'Use post request'})



@login_required
def downloads(request):
    return render(request, 'downloads.html')


@login_required
def new_updates(request):
    new_updates = NewUpdate.objects.all().order_by('-date')
    serializer = NewUpdateSerializer(new_updates, many=True)

    serialized_json = json.dumps(serializer.data, cls=DjangoJSONEncoder)


    context = {
        'new_updates': serialized_json
    }

    return render(request, 'new_updates.html', context=context)


@login_required
def add_new_update(request):
    if request.method=='POST':
        new_update = NewUpdate(description=request.POST['description'])
        new_update.save()

    return redirect(reverse('firstpage:new_updates'))



@login_required
def update_new_update(request):
    if request.method=='POST':
        new_update = NewUpdate.objects.get(id=request.POST['id'])
        new_update.description = request.POST['description']
        new_update.save()

    return redirect(reverse('firstpage:new_updates'))


@login_required
def delete_new_update(request):
    if request.method=='POST':
        new_update = NewUpdate.objects.get(id=request.POST['id'])
        new_update.delete()

    return redirect(reverse('firstpage:new_updates'))


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('firstpage:index'))