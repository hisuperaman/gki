from rest_framework import serializers
from .models import Student, Fee, Employee, EmployeeAttendance, NewUpdate
from django.db.models import Sum


class StudentSerializer(serializers.ModelSerializer):
    total_fee = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'  # Specify the fields to include in the serialized data

    def get_total_fee(self, obj):
        return obj.fee.aggregate(total=Sum('fee_amount'))['total'] or 0


class FeeSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    
    class Meta:
        model = Fee
        fields = '__all__'  # Specify the fields to include in the serialized data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  # Specify the fields to include in the serialized data


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    
    class Meta:
        model = EmployeeAttendance
        fields = '__all__'  # Specify the fields to include in the serialized data



class NewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUpdate
        fields = '__all__'  # Specify the fields to include in the serialized data