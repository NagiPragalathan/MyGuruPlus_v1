from django.shortcuts import render
from base.models import PathManager, FolderManager, McqQuestionBase, Config, UserSubscription, Comments, Rating
from django.db.models import Count
import random
def ListCourse(request, path):
    temp = []
    temp1=[]
    Files = PathManager.objects.filter(path=path)
    folders = FolderManager.objects.filter(path=path).order_by('FolderName')
    
    print(folders)
    mcq_questions = McqQuestionBase.objects.filter(path=path, question_type="MCQ")
    para_mcq_questions = McqQuestionBase.objects.filter(path=path, question_type="PARA")
    unique_para_categories_list = list(para_mcq_questions.values_list('quest_id', flat=True).distinct())
    unique_categories_list = list(mcq_questions.values_list('category', flat=True).distinct())
    Files = sorted(Files, key=lambda x: x.file.name)
    print(unique_para_categories_list)
    
    rating = {}  
    
        
    for i in folders:
        average_rating = Rating.calculate_average_rating(category=i.category)
        rating[i.category] = average_rating
        print(average_rating)
        
    for i in folders:
        i.rating = rating.get(i.category)
        print(i.category,rating.get(i.category))
        
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
    
    Subscription_path = []
    user_subs = UserSubscription.objects.filter(user_id=request.user)
    for i in FolderManager.objects.all():
        print("i.path", i.path)
    for i in user_subs:
        try:
            obj1 = PathManager.objects.get(path=i.course_premium)
            print(obj1)
            obj = FolderManager.objects.get(path=i.course_premium)
            print("course_premium",i.course_premium, obj.validity_days)
        except:
            print("Error at course_premium", i.course_premium)
        Subscription_path.append(i.course_premium.split('.')[1])
    mod_folder = []
    premium = []
    for i in folders:
        i.rating = rating.get(i.category)
        print(i.category, Subscription_path)
        if i.category not in Subscription_path:
            mod_folder.append(i)
        else:
            obj = UserSubscription.objects.get(course_premium="root."+str(i.category))
            folder_obj = FolderManager.objects.get(category=i.category)
            print("obj.is_premium_expired(folder_obj.validity_days)",obj.is_premium_expired(folder_obj.validity_days))
            print("premium : ",i.path, i.category, i.validity_days)
            if not obj.is_premium_expired(folder_obj.validity_days): # Here the code check the validity of subscription
                premium.append(i)
    print(premium, mod_folder)
    
    # comments !
    try:
        comments = Comments.objects.filter(category=path.split('.')[1])
        for i in comments:
            formatted_datetime = i.last_updated_date.strftime("%b. %d, %Y")
            i.last_updated_date = formatted_datetime
            i.first = i.user_id.username[0]
        user_exists = Rating.objects.filter(category=path.split('.')[1], user=request.user).exists()
    except Exception as e:
        comments = False
        user_exists = False
        print(e)

    if path != 'root':
        obj2 = FolderManager.objects.get(category=path.split('.')[1],  path='root')
        print(path, premium, path.split('.')[1], obj2.cost)
        
        
    if path == 'root':
        return render(request, 'UserView/ListCourse.html', {'path':path,'path_alter':path.replace(".", "/"),'star':[1,2,3,4,5],'auth':request.user.is_authenticated,
                                                        'path_list':out_path,'folders': mod_folder, 'files': Files,'user_exists':not user_exists,
                                                        'category':category, 'mcq':temp,'mcq_para':temp1, "premium" :premium, 'comments':comments})
    elif obj2.cost == 0 or (path.split('.')[1] in Subscription_path ) :
        return render(request, 'UserView/ListCourse_Folder.html', {'path':path,'path_alter':path.replace(".", "/"),'star':[1,2,3,4,5],'auth':request.user.is_authenticated,
                                                        'path_list':out_path,'folders': mod_folder, 'files': Files,'user_exists':not user_exists,
                                                        'category':category, 'mcq':temp,'mcq_para':temp1, "premium" :premium, 'comments':comments})
    else:
        return render(request, 'UserView/course_error.html',  {'path': obj2.id})
            
def free_courses(request, path, type):
    folders = FolderManager.objects.filter(path=path).order_by('FolderName')
    rating = {}
    for i in folders:
        average_rating = Rating.calculate_average_rating(category=i.category)
        rating[i.category] = average_rating
        print(average_rating)
    if type == 'free':
        folders = FolderManager.objects.filter(path=path, cost=0).order_by('FolderName')
    elif type == 'enrolled':
        Subscription_path = []
        user_subs = UserSubscription.objects.filter(user_id=request.user)
        for i in user_subs:
            Subscription_path.append(i.course_premium.split('.')[1])
        premium = []
        for i in folders:
            if i.category in Subscription_path:
                i.rating = rating.get(i.category)
                i.cost = "Owend"
                premium.append(i)
        folders = premium 
    return render(request, 'UserView/ListCourse.html', {'path':path,'path_alter':path.replace(".", "/"), 'premium': folders, 'star':[1,2,3,4,5],})

def show_instructions(request, path):
    mcq_questions = McqQuestionBase.objects.filter(question_type="MCQ", path=path)
    instructions_out= ""
    for i in mcq_questions:
        instructions_out = i.instructions
    obj = FolderManager.objects.all()
    print(path.split('.')[1])
    # obj1 = FolderManager.objects.get(category=path.split('.')[1])
    # print(obj1.validity_days)
    user_subscription= UserSubscription.objects.all()
    
    for i in user_subscription:
        print(i.course_premium)
    print("............................")
    
    for i in McqQuestionBase.objects.all():
        print(i.path)
    
    for i in obj:
        print(i.category,i.path)
    return render(request, 'question_manager/instructions.html',{'instructions':instructions_out, 'path':path})


def take_quiz(request, path):
    mcq_questions = McqQuestionBase.objects.filter(question_type="MCQ")
    mcq_questions_para = McqQuestionBase.objects.filter(
        question_type="PARA",
        path=path 
    )
    out_mcq = []
    for i in mcq_questions:
        if "," in i.copy_qust_path:
            if path in i.copy_qust_path.split(", "):
                out_mcq.append(i)
        else:
            if path == i.copy_qust_path:
                out_mcq.append(i)
    questions = []
    options = []
    explain = []
    correctAnswer = []
    question_ids = []

    # out = {"instructions":mcq_questions[0].instructions,"questions":[{'id':question.id,'question': question.question, 'options': question.options,'explain':question.explain,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in out_mcq]}
    for question in out_mcq:
        questions.append(question.question)
        options.append(question.options)
        explain.append(question.explain)
        man = question.correct_answer[-1]
        print(question.correct_answer, man)
        correctAnswer.append(question.options[int(man)-1])
        question_ids.append(question.id)
    print(questions, options, correctAnswer)
    grouped_questions = mcq_questions_para.values('quest_id').annotate(total_questions=Count('id')) 

    try:
        timmer = Config.objects.filter(q_path=path)[::-1][0].time_mis
    except:
        timmer = 5400
    print(path, timmer)
    # Now, `grouped_questions` contains the quest_id and the total count of questions for each quest_id
    for group in grouped_questions:
        obj = McqQuestionBase.objects.filter(
            quest_id=group['quest_id'],
            user_id=request.user
        )
        for i in obj:
            questions.append([i.question,i.instructions])
            options.append(i.options)
            explain.append(i.explain)
            man = i.correct_answer[-1]
            correctAnswer.append(i.options[int(man)-1])
            question_ids.append(i.id)
            
        print("obj: ", obj)
        quest_id = group['quest_id']
        total_questions = group['total_questions']
        print(f"Quest ID: {quest_id}, Total Questions: {total_questions}", correctAnswer)
        
    Subscription_path = []
    user_subs = UserSubscription.objects.filter(user_id=request.user)
    for i in FolderManager.objects.all():
        print("i.path", i.path)
    for i in user_subs:
        # try:
        # obj1 = PathManager.objects.get(category=i.course_premium)
        # print(obj1)
        obj = FolderManager.objects.get(category=i.course_premium.split('.')[1])
        print("course_premium",i.course_premium, obj.validity_days)
        # except:
        #     print("Error at course_premium", i.course_premium)
        Subscription_path.append(i.course_premium.split('.')[1])
    print(Subscription_path, path)
    
    correct_shuffle=[]
    for a,b,c,d,e in zip(questions, options, correctAnswer, question_ids, explain):
        correct_shuffle.append([a,b,c,d,e])
    random.shuffle(correct_shuffle)
    print(correct_shuffle)
    question = []
    option = []
    correctAnswers = []
    question_id = []
    explains = []
    
    for a,b,c,d,e in correct_shuffle:
        question.append(a)
        option.append(b)
        correctAnswers.append(c)
        question_id.append(d)
        explains.append(e)
        
    
    if path.split('.')[1] in Subscription_path:
        return render(request, "UserView/TakeQuiz.html",{'questions':question,'options':option, 'answers':correctAnswers, 'question_ids':question_id, "explain":explains, 'timmer':timmer, 'path':path, 'ads': False})
    else:
        return render(request, "UserView/TakeQuiz.html",{'questions':question,'options':option, 'answers':correctAnswers, 'question_ids':question_id, "explain":explains, 'timmer':timmer, 'path':path,'ads' : True})
        
