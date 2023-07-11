from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Department, Session_Year, CustomUser, Participant, Staff, Subject, Staff_Notification, \
    Staff_Leave, Participant_Notification, Participant_Leave,Attendance_Report,Attendance
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
import datetime


@login_required(login_url='/')
def HOME(request):
    participant_count = Participant.objects.all().count()
    staff_count = Staff.objects.all().count()
    department_count = Department.objects.all().count()
    subject_count = Subject.objects.all().count()
    participant_male = Participant.objects.filter(gender='Male').count()
    participant_female = Participant.objects.filter(gender='Female').count()
    staff_male = Staff.objects.filter(gender='Male').count()
    staff_female = Staff.objects.filter(gender='Female').count()
    context = {
        'participant_count': participant_count,
        'staff_count': staff_count,
        'department_count': department_count,
        'subject_count': subject_count,
        'participant_male': participant_male,
        'participant_female': participant_female,
        'staff_male': staff_male,
        'staff_female': staff_female,

    }

    return render(request, 'Hod/home.html', context)


@login_required(login_url='/')
def ADD_STUDENT(request):
    department = Department.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        session_year_id = request.POST.get('session_year_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()

            department = Department.objects.get(id=department_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            participant = Participant(
                admin=user,
                address=address,
                session_year_id=session_year,
                department_id=department,
                gender=gender,
            )
            participant.save()
            messages.success(request, user.first_name + "  " + user.last_name + " Are Successfully Added !")
            return redirect('add_student')

    context = {
        'department': department,
        'session_year': session_year,
    }

    return render(request, 'Hod/add_student.html', context)


@login_required(login_url='/')
def VIEW_STUDENT(request):
    participant = Participant.objects.all()

    context = {
        'participant': participant,
    }
    return render(request, 'Hod/view_student.html', context)


@login_required(login_url='/')
def EDIT_STUDENT(request, id):
    participant = Participant.objects.filter(id=id)
    department = Department.objects.all()
    session_year = Session_Year.objects.all()

    participant_male = Participant.objects.filter(gender='Male').count()
    participant_female = Participant.objects.filter(gender='Female').count()

    context = {
        'participant': participant,
        'department': department,
        'session_year': session_year,
        'participant_male': participant_male,
        'participant_female': participant_female,
    }
    return render(request, 'Hod/edit_student.html', context)


@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        print(student_id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = CustomUser.objects.get(id=student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        participant = Participant.objects.get(admin=student_id)
        participant.address = address
        participant.gender = gender

        department = Department.objects.get(id=course_id)
        participant.course_id = department

        session_year = Session_Year.objects.get(id=session_year_id)
        participant.session_year_id = session_year

        participant.save()
        messages.success(request, 'Record Are Successfully Updated !')
        return redirect('view_student')

    return render(request, 'Hod/edit_student.html')


@login_required(login_url='/')
def DELETE_STUDENT(request, admin):
    participant = CustomUser.objects.get(id=admin)
    participant.delete()
    messages.success(request, 'Record Are Successfully Deleted !')
    return redirect('view_student')


@login_required(login_url='/')
def ADD_DEPARTMENT(request):
    if request.method == "POST":
        department_name = request.POST.get('department_name')

        department = Department(
            name=department_name,
        )
        department.save()
        messages.success(request, 'Department Are Successfully Created ')
        return redirect('add_department')

    return render(request, 'Hod/add_department.html')


@login_required(login_url='/')
def VIEW_DEPARTMENT(request):
    department = Department.objects.all()
    context = {
        'department': department,
    }
    return render(request, 'Hod/view_department.html', context)


@login_required(login_url='/')
def EDIT_DEPARTMENT(request, id):
    department = Department.objects.get(id=id)
    context = {
        'department': department,
    }
    return render(request, 'Hod/edit_department.html', context)


@login_required(login_url='/')
def UPDATE_DEPARTMENT(request):
    if request.method == "POST":
        name = request.POST.get('name')
        department_id = request.POST.get('department_id')

        department = Department.objects.get(id=department_id)
        department.name = name
        department.save()
        messages.success(request, 'Department Updated Successfully')
        return redirect('view_department')
    return render(request, 'Hod/edit_department.html')


@login_required(login_url='/')
def DELETE_DEPARTMENT(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    messages.success(request, 'Department are Successfully Deleted')

    return redirect('view_department')


@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken')
            return redirect('add_staff')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                gender=gender,
            )
            staff.save()
            messages.success(request, user.first_name + "  " + user.last_name + " Are Successfully Added !")
            return redirect('add_staff')

    return render(request, 'Hod/add_staff.html')


@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()

    context = {
        'staff': staff,
    }
    return render(request, 'Hod/view_staff.html', context)


@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = Staff.objects.filter(id=id)

    context = {
        'staff': staff,
    }
    return render(request, 'Hod/edit_staff.html', context)


@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id=staff_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        staff = Staff.objects.get(admin=staff_id)
        staff.address = address
        staff.gender = gender

        staff.save()
        messages.success(request, 'Record Are Successfully Updated !')
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')


@login_required(login_url='/')
def DELETE_STAFF(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Record Are Successfully Deleted !')
    return redirect('view_staff')


@login_required(login_url='/')
def ADD_SUBJECT(request):
    department = Department.objects.all()
    staff = Staff.objects.all()
    subject_name = ""

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        staff_id = request.POST.get('staff_id')
        department_id = request.POST.get('department_id')
        pdf_file = request.FILES.get('pdf_file')  # Get the uploaded file

        department = Department.objects.get(id=department_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            name=subject_name,
            staff=staff,
            department=department,
            pdf_file=pdf_file,  # Assign the uploaded file to the field
        )
        subject.save()
        messages.success(request, 'Subject Added Successfully')
        return redirect('add_subject')

    context = {
        'department': department,
        'staff': staff,
    }
    return render(request, 'Hod/add_subject.html', context)


@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()
    context = {
        'subject': subject,
    }
    return render(request, 'Hod/view_subject.html', context)


@login_required(login_url='/')
def EDIT_SUBJECT(request, id):
    subject = Subject.objects.get(id=id)
    department = Department.objects.all()
    staff = Staff.objects.all()
    context = {
        'subject': subject,
        'department': department,
        'staff': staff,
    }
    return render(request, 'Hod/edit_subject.html', context)


@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        subject_id = request.POST.get('subject_id')
        department_id = request.POST.get('department_id')
        staff_id = request.POST.get('staff_id')

        department = Department.objects.get(id=department_id)
        staff = Staff.objects.get(id=staff_id)
        subject = Subject(
            id=subject_id,
            name=subject_name,
            department=department,
            staff=staff
        )
        subject.save()
        messages.success(request, 'Subject Updated Successfully')
        return redirect('view_subject')
    return render(request, 'Hod/edit_subject.html')


@login_required(login_url='/')
def DELETE_SUBJECT(request, id):
    subject = Subject.objects.get(id=id)
    subject.delete()
    messages.success(request, 'Subject are Successfully Deleted')

    return redirect('view_subject')


@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == "POST":
        start = request.POST.get('session_start')
        end = request.POST.get('session_end')

        session = Session_Year(
            session_start=start,
            session_end=end
        )
        session.save()
        messages.success(request, 'Session Are Successfully Created ')
        return redirect('add_session')

    return render(request, 'Hod/add_session.html')


@login_required(login_url='/')
def VIEW_SESSION(request):
    session = Session_Year.objects.all()
    context = {
        'session': session,
    }
    return render(request, 'Hod/view_session.html', context)


@login_required(login_url='/')
def EDIT_SESSION(request, id):
    session = Session_Year.objects.get(id=id)
    context = {
        'session': session,
    }
    return render(request, 'Hod/edit_session.html', context)


@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == "POST":
        start = request.POST.get('session_start')
        end = request.POST.get('session_end')
        session_id = request.POST.get('session_id')

        session = Session_Year(
            id=session_id,
            session_start=start,
            session_end=end
        )
        session.save()
        messages.success(request, 'Session Updated Successfully')
        return redirect('view_session')
    return render(request, 'Hod/edit_session.html')


@login_required(login_url='/')
def DELETE_SESSION(request, id):
    session = Session_Year.objects.get(id=id)
    session.delete()
    messages.success(request, 'Session are Successfully Deleted')

    return redirect('view_session')


def download_participants(request):
    # Fetch the student data from the database
    participants = Participant.objects.all()

    # Create a BytesIO buffer to store the PDF file
    buffer = BytesIO()

    # Create the PDF object
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set the PDF title
    pdf.setTitle("Participants Information")

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Print the current date and time on the top left
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(20, 770, current_datetime)

    # Print 'Liste des participants' on the top middle
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawCentredString(400, 770, 'Liste des participants')

    # Define the table data
    data = [['ID', 'First Name', 'Last Name', 'Email', 'Gender', 'Department']]

    # Populate the table data with participant information
    for participant in participants:
        row = [
            participant.id,
            participant.admin.first_name,
            participant.admin.last_name,
            participant.admin.email,
            participant.gender,
            participant.department_id.name,
        ]
        data.append(row)

    # Create the table
    table = Table(data, colWidths=[50, 100, 100, 150, 50, 100, 180])

    # Set the table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Get the table width and height
    table_width, table_height = table.wrapOn(pdf, 400, 600)

    # Calculate the X-coordinate to center the table horizontally
    x = (letter[0] - table_width) / 2

    # Set the table coordinates and draw it on the PDF
    table.drawOn(pdf, x, 500)

    # Save the PDF
    pdf.save()

    # Rewind the buffer's file pointer
    buffer.seek(0)

    # Create a HttpResponse object with the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}_participants.pdf"'.format(current_datetime)

    # Write the PDF buffer to the response
    response.write(buffer.getvalue())

    return response


def download_departments(request):
    departments = Department.objects.all()

    # Create a BytesIO buffer to store the PDF file
    buffer = BytesIO()

    # Create the PDF object
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set the PDF title
    pdf.setTitle("Departments Informations")

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Print the current date and time on the top left
    # Print the current date and time on the top left
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(20, 770, current_datetime)

    # Print 'Liste des participants' on the top middle
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawCentredString(400, 770, 'Liste des participants')

    # Define the table data
    data = [['ID', 'Name', 'Created at']]

    # Populate the table data with participant information
    for i in departments:
        row = [
            i.id,
            i.name,
            i.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ]
        data.append(row)

    # Create the table
    table = Table(data, colWidths=[50, 100, 100, 150, 50, 100, 180])

    # Set the table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Get the table width and height
    table_width, table_height = table.wrapOn(pdf, 400, 600)

    # Calculate the X-coordinate to center the table horizontally
    x = (letter[0] - table_width) / 2

    # Set the table coordinates and draw it on the PDF
    table.drawOn(pdf, x, 500)

    # Save the PDF
    pdf.save()

    # Rewind the buffer's file pointer
    buffer.seek(0)

    # Create a HttpResponse object with the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}_departments.pdf"'.format(current_datetime)

    # Write the PDF buffer to the response
    response.write(buffer.getvalue())

    return response


def download_staff(request):
    staff = Staff.objects.all()

    # Create a BytesIO buffer to store the PDF file
    buffer = BytesIO()

    # Create the PDF object
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set the PDF title
    pdf.setTitle("Staff Informations")

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Print the current date and time on the top left
    # Print the current date and time on the top left
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(20, 770, current_datetime)

    # Print 'Liste des participants' on the top middle
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawCentredString(400, 770, 'Liste des Staff')

    # Define the table data
    data = [['ID', 'First Name', 'Last Name', 'Email', 'Gender', 'Address']]

    # Populate the table data with participant information
    for i in staff:
        row = [
            i.id,
            i.admin.first_name,
            i.admin.last_name,
            i.admin.email,
            i.gender,
            i.address
        ]
        data.append(row)

    # Create the table
    table = Table(data, colWidths=[50, 100, 100, 150, 50, 100, 180])

    # Set the table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Get the table width and height
    table_width, table_height = table.wrapOn(pdf, 400, 600)

    # Calculate the X-coordinate to center the table horizontally
    x = (letter[0] - table_width) / 2

    # Set the table coordinates and draw it on the PDF
    table.drawOn(pdf, x, 500)

    # Save the PDF
    pdf.save()

    # Rewind the buffer's file pointer
    buffer.seek(0)

    # Create a HttpResponse object with the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}_staff.pdf"'.format(current_datetime)

    # Write the PDF buffer to the response
    response.write(buffer.getvalue())

    return response


def download_subjects(request):
    subjects = Subject.objects.all()

    # Create a BytesIO buffer to store the PDF file
    buffer = BytesIO()

    # Create the PDF object
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set the PDF title
    pdf.setTitle("Subjects Informations")

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Print the current date and time on the top left
    # Print the current date and time on the top left
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(20, 770, current_datetime)

    # Print 'Liste des participants' on the top middle
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawCentredString(400, 770, 'List of Subjects')

    # Define the table data
    data = [['ID', 'Name', 'Department', 'Staff']]

    # Populate the table data with participant information
    for i in subjects:
        row = [
            i.id,
            i.name,
            i.department,
            f"{i.staff.admin.first_name} {i.staff.admin.last_name}",
        ]
        data.append(row)

    # Create the table
    table = Table(data, colWidths=[50, 100, 100, 150, 50, 100, 180])

    # Set the table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Get the table width and height
    table_width, table_height = table.wrapOn(pdf, 400, 600)

    # Calculate the X-coordinate to center the table horizontally
    x = (letter[0] - table_width) / 2

    # Set the table coordinates and draw it on the PDF
    table.drawOn(pdf, x, 500)

    # Save the PDF
    pdf.save()

    # Rewind the buffer's file pointer
    buffer.seek(0)

    # Create a HttpResponse object with the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}_subjects.pdf"'.format(current_datetime)

    # Write the PDF buffer to the response
    response.write(buffer.getvalue())

    return response


def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all()
    context = {
        'staff': staff,
        'see_notification': see_notification,
    }
    return render(request, 'Hod/staff_notification.html', context)


def STAFF_SAVE_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=staff_id)
        notification = Staff_Notification(
            staff_id=staff,
            message=message
        )
        notification.save()
        messages.success(request, 'Notification Sent Successfully')
    return redirect('staff_send_notification')


def Staff_Leave_view(request):
    staff_leave = Staff_Leave.objects.all()
    context = {
        'staff_leave': staff_leave,
    }
    return render(request, 'Hod/staff_leave.html', context)


def Staff_approve_leave(request, id):
    leave = Staff_Leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')


def Staff_decline_leave(request, id):
    leave = Staff_Leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')


def PART_SEND_NOTIFICATION(request):
    participant = Participant.objects.all()
    notifications = Participant_Notification.objects.all()
    context = {
        'participant': participant,
        'notifications': notifications,
    }
    return render(request, 'Hod/part_notification.html', context)


def PART_SAVE_NOTIFICATION(request):
    if request.method == "POST":
        participant_id = request.POST.get('participant_id')
        message = request.POST.get('message')

        participant = Participant.objects.get(admin=participant_id)
        notification = Participant_Notification(
            participant_id=participant,
            message=message

        )
        notification.save()
        messages.success(request, 'Notification Sent Successfully')
    return redirect('participant_send_notification')


def Participant_Leave_view(request):
    participant_leave = Participant_Leave.objects.all()
    context = {
        'participant_leave': participant_leave,
    }
    return render(request, 'Hod/part_leave.html', context)


def Participant_approve_leave(request, id):
    leave = Participant_Leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('participant_leave_view')


def Participant_decline_leave(request, id):
    leave = Participant_Leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('participant_leave_view')


def HOD_VIEW_ATTENDANCE(request):

    subject = Subject.objects.all()
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    date_attendance = None
    attendance = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')
            date_attendance = request.POST.get('date_attendance')
            get_subject = Subject.objects.get(id=subject_id)
            get_session = Session_Year.objects.get(id=session_id)
            attendance = Attendance.objects.filter(subject_id=get_subject, attendance_data=date_attendance)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)
    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session,
        'date_attendance': date_attendance,
        'attendance': attendance,
        'attendance_report': attendance_report
    }
    return render(request, 'Hod/hod_view_attendance.html', context)