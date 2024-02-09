from django.shortcuts import render, redirect
from base.models import Report, McqQuestionBase

def is_superuser(user):
    return user.is_authenticated and user.is_superuser


def create_report(request, question_id):
    if request.method == 'POST':
        message = request.POST['message']

        Report.objects.create(user_id=request.user, message=message, question_id=question_id, flag='false')
        return redirect('list_reports')

    return render(request, 'Report/create_report.html')

def list_reports(request):
    reports = Report.objects.all()

    for report in reports:
        # Assuming there is a ForeignKey relationship from Report to McqQuestionBase
        mcq_question_base = McqQuestionBase.objects.get(id=report.question_id)
        report.q_path = mcq_question_base.path  # Add the 'q_path' attribute to the report object
        report.type = mcq_question_base.question_type  # Add the 'q_path' attribute to the report object
        if mcq_question_base.question_type == "PARA":
           report.quest_id = mcq_question_base.quest_id

    return render(request, 'Report/list_reports.html', {'reports': reports, 'is_superuser':is_superuser(request.user)})


def update_report(request, report_id):
    if request.method == 'POST':
        report = Report.objects.get(id=report_id)
        report.message = request.POST['message']
        report.flag = request.POST['flag']
        report.save()
        return redirect('list_reports')

    report = Report.objects.get(id=report_id)
    return render(request, 'Report/update_report.html', {'report': report})

def delete_report(request, report_id):
    report = Report.objects.get(id=report_id)
    report.delete()
    return redirect('list_reports')
