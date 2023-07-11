from django.shortcuts import render, redirect
from app.models import Department,Participant, Participant_Notification, Participant_Leave, Subject, Attendance, Attendance_Report
from django.contrib import messages


def HOME(request):
    participant = Participant.objects.filter(admin=request.user.id)
    context = {
        'participant':participant
    }
    return render(request, 'Participant/home.html',context)


def NOTIFICATIONS(request):
    participant = Participant.objects.filter(admin=request.user.id)
    for i in participant:
        participant_id = i.id
        notification = Participant_Notification.objects.filter(participant_id=participant_id)
        context = {
            'notification': notification,
        }
    return render(request, 'Participant/Notifications.html', context)


def part_mark_as_seen(request, status):
    notification = Participant_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()

    return redirect('participant_notifications')


def PART_APPLY_LEAVE(request):
    return render(request, 'Participant/part_apply_leave.html')


def PART_APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        participant = Participant.objects.get(admin=request.user.id)
        leave = Participant_Leave(
            participant_id=participant,
            data=leave_date,
            message=leave_message

        )
        messages.success(request, 'Leave Applied Successfully')
        leave.save()

    return redirect('part_apply_leave')


def VIEW_ATTENDANCE(request):
    participant = Participant.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(department=participant.department_id)
    action = request.GET.get('action')
    get_subject = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)
            attendance_report = Attendance_Report.objects.filter(participant_id=participant,
                                                                 attendance_id__subject_id=subject_id)
    context = {
        'subjects': subjects,
        'action': action,
        'get_subject': get_subject,
        'attendance_report': attendance_report

    }
    return render(request, 'Participant/view_attendance.html', context)


def VIEW_SUBJECT(request):
    participant = Participant.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(department=participant.department_id)

    context = {
        'subjects': subjects,
    }

    return render(request, 'Participant/participant_view_subject.html', context)

