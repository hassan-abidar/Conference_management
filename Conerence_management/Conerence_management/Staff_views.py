from django.shortcuts import render, redirect
from app.models import Staff, Staff_Notification, Staff_Leave, Subject, Session_Year, Participant, Attendance, \
    Attendance_Report
from django.contrib import messages


def HOME(request):
    staff = Staff.objects.filter(admin=request.user.id)
    context = {
        'staff': staff
    }
    return render(request, 'Staff/home.html', context)


def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        notification = Staff_Notification.objects.filter(staff_id=staff_id)
        context = {
            'notification': notification,
        }
    return render(request, 'Staff/Notifications.html', context)


def mark_as_seen(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()

    return redirect('staff_notifications')


def APPLY_LEAVE(request):
    return render(request, 'Staff/apply_leave.html')


def APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        staff = Staff.objects.get(admin=request.user.id)
        leave = Staff_Leave(
            staff_id=staff,
            data=leave_date,
            message=leave_message

        )
        messages.success(request, 'Leave Applied Successfully')
        leave.save()

    return redirect('apply_leave')


def STAFF_TAKE_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff=staff_id)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    participants = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')
            get_subject = Subject.objects.get(id=subject_id)
            get_session = Session_Year.objects.get(id=session_id)
            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                participant_id = i.department.id
                participants = Participant.objects.filter(department_id=participant_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session': get_session,
        'action': action,
        'participants': participants
    }
    return render(request, 'Staff/staff_take_attendance.html', context)


def STAFF_SAVE_ATTENDANCE(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')
        attendance_date = request.POST.get('attendance_date')
        participant_id = request.POST.getlist('participant_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session = Session_Year.objects.get(id=session_id)
        attendance = Attendance(
            subject_id=get_subject,
            attendance_data=attendance_date,
            session_year_id=get_session)
        attendance.save()
        for i in participant_id:
            part_id = i
            int_part = int(part_id)
            p_participants = Participant.objects.get(id=int_part)
            attendance_report = Attendance_Report(
                participant_id=p_participants,
                attendance_id=attendance,
            )
            attendance_report.save()
        messages.success(request, 'Attendance Applied Successfully')

    return redirect('staff_take_attendance')


def STAFF_VIEW_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff_id=staff_id)
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
    return render(request, 'Staff/staff_view_attendance.html', context)


def STAFF_VIEW_SUBJECT(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff=staff_id)
    context = {
        'subject': subject,
    }
    return render(request, 'Staff/staff_view_subject.html', context)
