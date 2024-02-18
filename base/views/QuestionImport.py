from django.shortcuts import render
import csv
import io
from base.models import McqQuestionBase

def process_csv_file(csv_file):
    csv_data = []
    
    # Use io.TextIOWrapper to open the file in text mode
    with io.TextIOWrapper(csv_file, encoding='utf-8', newline='') as file_wrapper:
        csv_reader = csv.DictReader(file_wrapper)
        
        for row in csv_reader:
            csv_data.append(row)
    return csv_data


def process_csv(request, path):
    if request.method == 'POST' and request.FILES['csv_file']:
        splited_char = "\n" #you can also use "," here
        csv_file = request.FILES['csv_file']
        Instructions = request.POST.get('inst')

        # Process the CSV file
        csv_data = process_csv_file(csv_file)

        # Print CSV data to console
        for row in csv_data:
            print(row)
        for data in csv_data: 
            print(Instructions)                     # _/
            print(data.get('Question'))             # _/
            print(data.get('Explanation'))          # _/
            print(data.get('Options').split(splited_char))  # _/
            print(data.get('CorrectAnswer'))
            print(data.get('CorrectAnswer'),data.get('Options').split(splited_char)[int(data.get('CorrectAnswer'))-1],"option"+data.get('CorrectAnswer'))
            print("option"+data.get('CorrectAnswer'))
            question, created = McqQuestionBase.objects.get_or_create(
                question=data.get('Question'),
                path=path,
                user_id = request.user,
                copy_qust_path=path,
                defaults={
                    'instructions': Instructions,
                    'options': data.get('Options').split(splited_char),
                    'explain': data.get('Explanation'),
                    'correct_answer': "option"+str(data.get('CorrectAnswer')),
                    'question_type': 'MCQ',  # You might want to adjust this based on your requirements
                    'category': path.split('.')[1],  # Adjust the category as needed
                }
            )
            correct_answer = "option" + str(data.get('CorrectAnswer'))
            print(correct_answer)
            # If the question already existed, update its fields
            if not created:
                question.instructions = Instructions
                question.options = data.get('Options').split(splited_char)
                question.explain = data.get('Explanation')
                question.save()
                
        obj = McqQuestionBase.objects.all()
        for i in obj:
            print(i.question,i.options, i.explain, i.correct_answer, i.instructions)

        return render(request, 'message.html', {'path':path})

    return render(request, 'upload_csv.html')
