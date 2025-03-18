from django.shortcuts import render
from django.http import HttpResponse
from .models import Dept, Emp
from datetime import datetime
from django.db.models import Q

# Function to insert a department using input()
def insert_department(request=None):  # request is optional for manual execution
    deptno = input("Enter Department Number: ")
    dname = input("Enter Department Name: ")
    loc = input("Enter Location: ")

    if deptno.isdigit() and dname and loc:
        deptno = int(deptno)
        existing_dept = Dept.objects.filter(deptno=deptno).first()

        if existing_dept:
            return HttpResponse(f"⚠️ Department '{dname}' already exists!")
        else:
            Dept.objects.create(deptno=deptno, dname=dname, loc=loc)
            return HttpResponse(f"✅ Department '{dname}' inserted successfully!")

    return HttpResponse("❌ Error: Invalid input! Please enter valid values.", status=400)
# insert_department()

# Function to insert an employee using input()
def insert_employee(request=None):  # request is optional for manual execution
    empno = input("Enter Employee Number: ")
    ename = input("Enter Employee Name: ")
    job = input("Enter Job Title: ")
    mgr = input("Enter Manager ID (Enter 0 if no manager): ")
    hiredate_str = input("Enter Hire Date (YYYY-MM-DD): ")
    sal = input("Enter Salary: ")
    comm = input("Enter Commission (Enter 0 if none): ")
    deptno = input("Enter Department Number: ")

    # Validate required fields
    if empno.isdigit() and ename and job and hiredate_str and sal.replace('.', '', 1).isdigit() and deptno.isdigit():
        empno = int(empno)
        mgr = int(mgr) if mgr.isdigit() else None
        sal = float(sal)
        comm = float(comm) if comm else 0.0
        hiredate = datetime.strptime(hiredate_str, "%Y-%m-%d").date()
        deptno = int(deptno)

        dept = Dept.objects.filter(deptno=deptno).first()

        if dept:
            existing_emp = Emp.objects.filter(empno=empno).first()

            if existing_emp:
                return HttpResponse(f"⚠️ Employee '{ename}' already exists!")
            else:
                Emp.objects.create(
                    empno=empno,
                    ename=ename,
                    job=job,
                    mgr=mgr,
                    hiredate=hiredate,
                    sal=sal,
                    comm=comm,
                    deptno=dept
                )
                return HttpResponse(f"✅ Employee '{ename}' added successfully!")
        else:
            return HttpResponse("❌ Error: Department not found!", status=404)

    return HttpResponse("❌ Error: Invalid input! Please enter valid values.", status=400)
# insert_employee()

# Function to retrieve employee data using input()
# def retrieve_employee(request=None):  # request is optional for manual execution
#     emp_id = input("Enter Employee Number to Retrieve: ")

#     if emp_id.isdigit():
#         emp_id = int(emp_id)
#         emp = Emp.objects.filter(empno=emp_id).first()

#         if emp:
#             return HttpResponse(
#                 f"✅ Employee Found: <br>"
#                 f"👤 Name: {emp.ename} <br>"
#                 f"💼 Job: {emp.job} <br>"
#                 f"💲 Salary: {emp.sal} <br>"
#                 f"🏢 Department: {emp.deptno.dname}"
#             )
#         else:
#             return HttpResponse("❌ Employee not found!", status=404)

#     return HttpResponse("❌ Error: Invalid Employee Number!", status=400)
def retrieve_employees(request=None):
    employees = Emp.objects.all().order_by('ename')  # Get all employees
    developer = Emp.objects.filter(deptno=7561).order_by('ename')  # Get all employees
    departments = Dept.objects.all().order_by('dname')  # Get all departments
    bhubaneswardept = Dept.objects.filter(loc='Bhubaneswar')
    otherdept = Dept.objects.filter(Q(loc='Bengaluru') | Q(loc='Kolkata') | Q(loc='Pune') | Q(loc='Hyderabad'))
    return render(request, 'employees.html', {'employees': employees, 'developer': developer, 'departments': departments, 'bhubaneswardept':bhubaneswardept, 'otherdept':otherdept})

