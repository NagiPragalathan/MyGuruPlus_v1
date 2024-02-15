from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from base.models import FolderManager, Rating, LatestUpdate, Contact

def home(request):
    folders = FolderManager.objects.filter(path='root').order_by('FolderName')[::-1]
    rating = {}
    updates = LatestUpdate.objects.all()[::-1]
    
        
    for i in folders:
        average_rating = Rating.calculate_average_rating(category=i.category)
        rating[i.category] = average_rating
        print(average_rating)
    for i in folders:
        i.rating = rating.get(i.category)
        print(i.category,rating.get(i.category), i.rating)
    
    if len(folders) > 4:
        folders = folders[0:4]
    
    if request.user.is_authenticated:
        login = True
    else:
        login = False
        
    if request.user.is_superuser:
        return redirect('list_folders', path='root')
    else:
        try:
            return render(request, "home/index.html", {'auth':login, 'courses':folders, 'rate':[1,2,3,4,5], 'updates':updates[0].message})
        except:
            return render(request, "home/index.html", {'auth':login, 'courses':folders, 'rate':[1,2,3,4,5], 'updates':"🆕 Last Updates"})
            
def home2(request):
    folders = FolderManager.objects.filter(path='root').order_by('FolderName')[::-1]
    rating = {}
    updates = LatestUpdate.objects.all()[::-1]
    
        
    for i in folders:
        average_rating = Rating.calculate_average_rating(category=i.category)
        rating[i.category] = average_rating
        # print(average_rating)
    for i in folders:
        i.rating = rating.get(i.category)
        # print(i.category,rating.get(i.category), i.rating)
    
    if len(folders) > 4:
        folders = folders[0:4]
    
    if request.user.is_authenticated:
        login = True
    else:
        login = False
        
    obj = Contact.objects.all()
    for i in obj:
        print(i.message, i.name)
    try:
        return render(request, "home/index.html", {'auth':login, 'courses':folders, 'rate':[1,2,3,4,5],'updates':updates[0].message})
    except:
        return render(request, "home/index.html", {'auth':login, 'courses':folders, 'rate':[1,2,3,4,5], 'updates':"🆕 Last Updates"})
        
def logout_view(request):
    logout(request)
    return redirect('home')

def about_us(request):
    return  render(request,"Common/ABOUT_US.html")

def disclaimer(request):
    return  render(request,"Common/Disclaimer.html")

def private_policy(request):
    return  render(request,"Common/Privacy_Policy.html")

def return_and_refund(request):
    return  render(request,"Common/RETURN_AND_REFUND_POLICY.html")

def terms_and_condition(request):
    return  render(request,"Common/Terms_and_Conditions.html")

def contact_us(request):
    return  render(request,"Common/contact_us.html")

def test(request):
    return  render(request,"test.html")

def test1(request):
    return  render(request,"test1.html")
