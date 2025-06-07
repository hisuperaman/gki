from django.db import models

class Student(models.Model):
    rollnumber = models.AutoField(primary_key=True)
    pfp = models.ImageField(upload_to='images/')
    fullname = models.CharField(max_length=400, default=None, null=False)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    mobile_number = models.IntegerField()
    gender = models.CharField(max_length=200)
    fathername = models.TextField()
    address = models.TextField()
    class10_details = models.JSONField()
    class12_details = models.JSONField()
    graduation_details = models.JSONField()
    masters_details = models.JSONField()
    courses_applied = models.JSONField()
    enrollment_date = models.DateField(auto_now_add=True)

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee')
    
    receipt_number = models.IntegerField()
    fee_amount = models.IntegerField()
    deposit_date = models.DateField()


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    pfp = models.ImageField(upload_to='images/')
    fullname = models.CharField(max_length=400, default=None, null=False)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    mobile_number = models.IntegerField()
    gender = models.CharField(max_length=200)
    address = models.TextField()
    class10_details = models.JSONField()
    class12_details = models.JSONField()
    graduation_details = models.JSONField()
    masters_details = models.JSONField()
    joining_date = models.DateField()


class EmployeeAttendance(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)


class NewUpdate(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()