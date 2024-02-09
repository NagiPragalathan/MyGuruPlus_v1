from django.shortcuts import render, redirect
from base.models import PathManager, FolderManager, McqQuestionBase
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def add_data(request):
    if request.method == 'POST':
        path = request.POST.get('path')
        file = request.FILES.get('file')  # Assuming file is submitted in the form
        title = request.POST.get('title')
        

        PathManager.objects.create(
            user_id=request.user,
            path=path,
            file=file,
            category=path.split('.')[1],
            title=title
        )
            
        sample = PathManager.objects.filter(user_id=request.user)
        for i in sample:
            print(i.path,i.file)

        return redirect('list_folders',path=path)  # Redirect to the list_data view after successful submission

    return render(request, 'file_manager/add_data.html')

def list_data(request):
    data_entries = PathManager.objects.all()
    return render(request, 'file_manager/list_data.html', {'data_entries': data_entries})



def add_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        category = request.POST.get('category')
        path = request.POST.get('path')
        file = request.FILES.get('file')  # Assuming file is submitted in the form
        description = request.POST.get('description','No description is provided for this course')
        cost = request.POST.get('cost','0')
        days = request.POST.get('validity','30')
        
        print("category", category, "title",folder_name)

        if path == 'root':
            FolderManager.objects.create(
                user_id=request.user,
                FolderName=folder_name,
                validity_days = days,
                category=folder_name,
                FolderImage = file,
                description=description,
                cost=cost,
                path=path
            )
        else:
            FolderManager.objects.create(
                user_id=request.user,
                FolderName=folder_name,
                description=description,
                FolderImage = file,
                cost=cost,
                category=path.split('.')[1],
                path=path
            )

        return redirect('list_folders',path=path)  # Redirect to the list_folders view after successful submission

    return render(request, 'file_manager/add_folder.html')

def list_folders(request, path):
    user = request.user
    temp = []
    temp1=[]
    Files = PathManager.objects.filter(path=path)
    folders = FolderManager.objects.filter(path=path).order_by('FolderName')
    mcq_questions = McqQuestionBase.objects.filter(path=path, question_type="MCQ")
    para_mcq_questions = McqQuestionBase.objects.filter(path=path, question_type="PARA")
    unique_para_categories_list = list(para_mcq_questions.values_list('quest_id', flat=True).distinct())
    unique_categories_list = list(mcq_questions.values_list('category', flat=True).distinct())
    Files = sorted(Files, key=lambda x: x.file.name)
    print(unique_para_categories_list)
    for file in Files:
        file_extension = file.file.name.split('.')[-1].lower()
        if file_extension.lower() in ['jpg', 'png', 'gif', 'jpeg', 'svg', 'webp', 'ico']:
            file.icon_path = file.file.url  # Adjust the path as needed
        else:
            file.icon_path = f'/static/images/Folders/{file_extension}.png'  # Adjust the path as needed
        file.type = file_extension
        file.title_name = file.title + "." + file_extension
    
    category = [i.FolderName for i in FolderManager.objects.filter(path="root").order_by('FolderName')]

    for i in unique_categories_list:
        print(i)
        # Create a new dictionary in each iteration
        current_mcq_out = {}
        current_mcq_out['name'] = i
        current_mcq_out['icon'] = f'/static/images/Folders/mcq.jpg'
        temp.append(current_mcq_out)
    for i in unique_para_categories_list:
        print(i)
        # Create a new dictionary in each iteration
        current_mcq_out = {}
        current_mcq_out['name'] = i
        current_mcq_out['icon'] = f'/static/images/Folders/para_mcq.png'
        temp1.append(current_mcq_out)
        
    out = ""
    path_list = []
    out_path = {}
    for i in path.split("."):
        out = out + i + "."
        path_list.append(out)
    path_list = [s[:-1] if s.endswith('.') else s for s in path_list]
    for i,j in zip(path_list,path.split('.')):
        out_path[j] = i
    
        
    print(category)
    
    if request.user.is_superuser:
        return render(request, 'file_manager/Manager.html', {'path':path,'path_alter':path.replace(".", "/"),
                                                         'path_list':out_path,'folders': folders, 'files': Files,
                                                         'category':category, 'mcq':temp,'mcq_para':temp1})
    else:
        return render(request, 'UserView/admin_error.html')


def edit_folder(request, folder_id, path):
    folder = FolderManager.objects.get(id=folder_id)

    if request.method == 'POST':
        folder.FolderName = request.POST.get('FolderName')
        folder.category = request.POST.get('category')
        folder.path = request.POST.get('path')
        folder.cost = request.POST.get('cost')
        folder.validity_days = request.POST.get('validity_days')
        folder.description = request.POST.get('description')

        # Handle file upload if provided
        if 'FolderImage' in request.FILES:
            folder.FolderImage = request.FILES['FolderImage']

        folder.save()
        return redirect('list_folders', path=path)

    return render(request, 'file_manager/edit_folder.html', {'folder': folder})


def delete_folder(request, folder_id, path):
    folder = get_object_or_404(FolderManager, id=folder_id)
    if request.method == 'GET':
        folder.delete()
        messages.success(request, 'Folder deleted successfully.')
        return redirect('list_folders', path=path)
    return redirect('list_folders', path=path)
