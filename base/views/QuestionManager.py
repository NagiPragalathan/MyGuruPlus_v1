from django.shortcuts import render, redirect, get_object_or_404
from base.models import McqQuestionBase, ImageEditor
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import uuid
import json
from django.db.models import Count, F
from itertools import groupby
import random

def add_question(request, path):
    for i in McqQuestionBase.objects.all():
        print(i.path,i.copy_qust_path)
    result = (
        McqQuestionBase.objects
        .values('path', 'id', 'user_id', 'question', 'image', 'category', 'question_type', 'options', 'correct_answer', 'instructions', 'copy_qust_path', 'last_updated_date')
        .annotate(count=Count('id'))
        .annotate(path_value=F('path'))
        .filter(path_value__isnull=False)
    )

    # Group the results by path_value
    grouped_data = {key: list(group) for key, group in groupby(result, key=lambda x: x['path_value'])}
    print(result)
    # Group the results by path_value
    # grouped_data = {key: list(group) for key, group in groupby(result, key=lambda x: x['path_values'])}
    # Pass the grouped_data to the template
    if request.user.is_superuser:
        return render(request, 'question_manager/add_questions.html', {"grouped_data": grouped_data, "path": path})
    else:
        return render(request, 'UserView/admin_error.html')



def add_para_question(request,path):
    if request.user.is_superuser:
        return render(request, 'question_manager/para_create.html',{"path":path})
    else:
        return render(request, 'UserView/admin_error.html')


@csrf_exempt  # Use this decorator for simplicity; consider using CSRF protection in production
def delete_question(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        questions_id = data.get('qid', '')
        path = data.get('path', '')
        if questions_id != '':
            question = get_object_or_404(McqQuestionBase, id=questions_id)
        else:
            return JsonResponse({'message': 'Question was not deleted. choose correct question to delete !'})
            

        if "," in question.copy_qust_path:
            copy_qust_path = [item.strip() for item in question.copy_qust_path.split(',')]
            copy_qust_path.remove(path)
            question.copy_qust_path = ", ".join(copy_qust_path)
            question.save()
        else:
            question.delete()

        return JsonResponse({'message': 'Question deleted successfully!', 'question': questions_id})
    else:
        return JsonResponse({'message': 'Question was not deleted!'})

def edit_question(request,path):
    mcq_questions = McqQuestionBase.objects.filter(question_type="MCQ")
    out_mcq = []
    instructions_out= ""
    for i in mcq_questions:
        instructions_out = i.instructions
        print(i.copy_qust_path, i.id, i.question, i.instructions, mcq_questions[0].instructions, mcq_questions[0].question)
    print(f"==================================={path}===============================================")
    for i in mcq_questions:
        if "," in i.copy_qust_path:
            if path in i.copy_qust_path.split(", "):
                print(i.copy_qust_path, i.id, i.question, i.explain,"explain")
                out_mcq.append(i)
        else:
            if path == i.copy_qust_path:
                print(i.copy_qust_path, i.id, i.question, i.explain, "explain")
                out_mcq.append(i)
    print(out_mcq)
    out = {"instructions":instructions_out,"questions":[{'id':question.id,'question': question.question,'options': question.options,'explain':question.explain,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in out_mcq]}
    print(out,len(out))
    
    
    result = (
        McqQuestionBase.objects
        .values('path', 'id', 'user_id', 'question', 'explain', 'image', 'category', 'question_type', 'options', 'correct_answer', 'instructions', 'copy_qust_path', 'last_updated_date')
        .annotate(count=Count('id'))
        .annotate(path_value=F('path'))
        .filter(path_value__isnull=False)
        .exclude(path=path)
    )
        # .exclude(copy_qust_path_value__contains=',')  # Exclude items with a comma

    # Group the results by path_value
    grouped_data = {key: list(group) for key, group in groupby(result, key=lambda x: x['path_value'])}
    # Serialize the questions to JSON format
    if request.user.is_superuser:
        if mcq_questions.exists():
            out = {"instructions":instructions_out,"questions":[{'id':question.id,'question': question.question,'explain':question.explain,'options': question.options,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in out_mcq]}
            print(out)
            return render(request, 'question_manager/edit_questions.html', {"path": path, 'mcq_quiz': out,"grouped_data": grouped_data})
        else:
            # Handle the case when no questions are found
            return render(request, 'question_manager/edit_questions.html', {"path": path, 'mcq_quiz': None})
    else:
        return render(request, 'UserView/admin_error.html')


def para_edit_question(request,path, cat):
    mcq_questions = McqQuestionBase.objects.filter(copy_qust_path=path, quest_id=cat)
    instructions_out = ""
    for i in mcq_questions:
        instructions_out = i.instructions
    # Serialize the questions to JSON format
    if request.user.is_superuser:
        if mcq_questions.exists():
            out = {"instructions":instructions_out,"questions":[{'id':question.id,'question': question.question,'options': question.options,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in mcq_questions]}
            return render(request, 'question_manager/para_quest.html', {"path": path, 'mcq_quiz': out,"cat":cat})
        else:
            # Handle the case when no questions are found
            return render(request, 'question_manager/para_quest.html', {"path": path, 'mcq_quiz': None})
    else:
        return render(request, 'UserView/admin_error.html')

@csrf_exempt
def update_db(request):
    try:
        # Hardcoded data for testing
        data = {}
        data = json.loads(request.body.decode('utf-8'))

        # Extract data from the JSON
        instructions = data.get('instructions', '')
        questions_data = data.get('questions', [])
        path = data.get('path', '')
        if instructions != '':
            for question_data in questions_data:
                question_text = question_data.get('question', '')
                explain = question_data.get('explain', 'Explanation not provided for this question')
                options = question_data.get('options', [])
                correct_answer = question_data.get('correctAnswer', '')
                print(explain, question_text)
                print("options from front end",options)

                # Construct the options array (remove null values)
                options = [option for option in options if option is not None]
                print("options from back end before update : ",options)

                # Find or create the McqQuestionBase object
                question, created = McqQuestionBase.objects.get_or_create(
                    question=question_text,
                    path=path,
                    user_id = request.user,
                    copy_qust_path=path,
                    defaults={
                        'instructions': instructions,
                        'options': options,
                        'explain': explain,
                        'correct_answer': correct_answer,
                        'question_type': 'MCQ',  # You might want to adjust this based on your requirements
                        'category': path.split('.')[1],  # Adjust the category as needed
                    }
                )

                # If the question already existed, update its fields
                if not created:
                    question.instructions = instructions
                    question.options = options
                    explain = explain
                    question.correct_answer = correct_answer,
                    question.save()
        obj = McqQuestionBase.objects.all()
        for i in obj:
            print(i.path,i.copy_qust_path, i.explain)

        return JsonResponse({'success': True, 'message': 'Data received and processed successfully','path':path})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def update_para_db(request):
    try:
        # Hardcoded data for testing
        data = {}
        data = json.loads(request.body.decode('utf-8'))
        unique_id = uuid.uuid4()

        # Extract data from the JSON
        Mail_question = data.get('instructions', '')
        questions_data = data.get('questions', [])
        path = data.get('path', '')
        if Mail_question != '':
            for question_data in questions_data:
                question_text = question_data.get('question', '')
                options = question_data.get('options', [])
                correct_answer = question_data.get('correctAnswer', '')

                # Construct the options array (remove null values)
                options = [option for option in options if option is not None]

                # Find or create the McqQuestionBase object
                question, created = McqQuestionBase.objects.get_or_create(
                    question=question_text,
                    path=path,
                    quest_id = unique_id,
                    user_id = request.user,
                    copy_qust_path=path,
                    defaults={
                        'instructions': Mail_question,
                        'options': options,
                        'Para_quest':Mail_question,
                        'correct_answer': correct_answer,
                        'question_type': 'PARA',  # You might want to adjust this based on your requirements
                        'category': path.split('.')[1],  # Adjust the category as needed
                    }
                )

                # If the question already existed, update its fields
                if not created:
                    question.instructions = Mail_question
                    question.options = options
                    question.correct_answer = correct_answer,
                    question.save()
        obj = McqQuestionBase.objects.filter(question_type="PARA")
        for i in obj:
            print(i.path,i.copy_qust_path)

        return JsonResponse({'success': True, 'message': 'Data received and processed successfully', 'u_id':unique_id,"path":path})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def get_questions_by_category(request, category):
    try:
        # Query the database to retrieve questions by category
        questions = McqQuestionBase.objects.filter(category=category)

        # Serialize the questions to JSON format
        serialized_questions = [{
            'id': question.id,
            'question': question.question,
            'options': question.options,
            'correct_answer': question.correct_answer,
            'instructions': question.instructions,
            'last_updated_date': question.last_updated_date,
        } for question in questions]

        return JsonResponse({'questions': serialized_questions})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    
    
@csrf_exempt
def handle_questions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        instructions = data.get('instructions', '')
        questions_data = data.get('questions', [])
        path = data.get('path', '')
        obj = McqQuestionBase.objects.all()
        for i in obj:
            print("in check : ",i.path,i.copy_qust_path, i.explain)
        
        print(questions_data, instructions, len(questions_data))
        print("instructions",instructions)
        for question_data in questions_data:
            question_id = question_data.get('id', None)
            question_text = question_data.get('question', '')
            explain = question_data.get('explain', 'Explanation not provided for this question')
            options = question_data.get('options', [])
            correct_answer = question_data.get('correctAnswer', '')
            
            # print(path, len(path),"question_text", question_text, len(question_text))
            # You may need to adjust the category and path values based on your requirements
            category = path.split('.')[1]
            
            if len(question_text) > 9:
                # Create or update McqQuestionBase instance
                # print("question_id :", question_id)
                if question_id and question_id != 'none':
                    # Update existing question
                    question = McqQuestionBase.objects.get(pk=question_id)
                    question.question = question_text
                    question.explain = explain
                    question.options = options
                    question.correct_answer = correct_answer
                    question.instructions = instructions
                    question.last_updated_date = timezone.now()
                    question.save()
                    # print(question.question,"are updated...!")
                else:
                    question, created = McqQuestionBase.objects.get_or_create(
                        question=question_text,
                        path=path,
                        user_id = request.user,
                        copy_qust_path=path,
                        defaults={
                            'instructions': instructions,
                            'options': options,
                            'explain': explain,
                            'correct_answer': correct_answer,
                            'question_type': 'MCQ',  # You might want to adjust this based on your requirements
                            'category': path.split('.')[1],  # Adjust the category as needed
                        }
                    )

                    # If the question already existed, update its fields
                    if not created:
                        question.instructions = instructions
                        question.options = options
                        explain = explain
                        question.correct_answer = correct_answer,
                        question.save()
                    
                    print("question are created..!")
            else:
                return JsonResponse({'error': f'The question ("{question_text}") should be more than 11 characters.'}, status=400)
        obj = McqQuestionBase.objects.all()
        for i in obj:
            print(i.question, i.explain, i.options)
        return JsonResponse({'message': 'Data processed successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def handle_para_questions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        instructions = data.get('instructions', '')
        questions_data = data.get('questions', [])
        path = data.get('path', '')
        cat = data.get('cat', '')
        
        print(questions_data, instructions, cat)

        for question_data in questions_data:
            question_id = question_data.get('id', None)
            question_text = question_data.get('question', '')
            options = question_data.get('options', [])
            correct_answer = question_data.get('correctAnswer', '')
            
            print(path)
            # You may need to adjust the category and path values based on your requirements
            category = path.split('.')[1]
            
            if len(question_text) > 9:

                # Create or update McqQuestionBase instance
                if question_id and question_id != 'none':
                    # Update existing question
                    question = McqQuestionBase.objects.get(pk=question_id)
                    question.question = question_text
                    question.options = options
                    question.correct_answer = correct_answer
                    question.instructions = instructions
                    question.last_updated_date = timezone.now()
                    question.save()
                    print(question.question,"are updated...!")
                else:
                    # Create new question
                    McqQuestionBase.objects.create(
                        user_id=request.user,
                        question=question_text,
                        options=options,
                        correct_answer=correct_answer,
                        instructions=instructions,
                        category=category,
                        path=path,
                        copy_qust_path = path,
                        quest_id = cat
                    )
            else:
                return JsonResponse({'error': f'The question ("{question_text}") should be more than 11 characters.'}, status=200)


        return JsonResponse({'message': 'Data processed successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def import_questions(request):
     if request.method == 'POST':
        data = json.loads(request.body)
        path = data.get('path', '')
        ids = data.get('ids', [])
        print(path,ids)
        for i in ids:
            question = McqQuestionBase.objects.get(id=i)
            if path not in question.path.split(','):
                new_path = question.path +", "+ path
                question.copy_qust_path = new_path
                question.last_updated_date = timezone.now()
                question.save()
            else:
                continue
        for i in ids:
            question = McqQuestionBase.objects.get(id=i)
            print(question.copy_qust_path)
        return JsonResponse({'message': 'Data processed successfully','path':path}, status=200)    
    
    
def add_image_editor(request):
    if request.method == 'POST':
        question_text = request.POST.get('question', '')
        # You may want to do additional processing here if needed
        ImageEditor.objects.create(question=question_text)
        return JsonResponse({'message': 'Data processed successfully'}, status=200)
    
    