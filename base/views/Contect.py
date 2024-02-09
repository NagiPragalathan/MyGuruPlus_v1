from django.shortcuts import render, redirect
from base.models import Contact
from django.utils import timezone

def submit_contact_form(request):
    print(request.method, 'called')
    if request.method == 'POST':
        print(request.POST)  # Print the POST data to console for debugging
        print("inner")
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        last_update = timezone.now()
        print(name, email, subject, message)
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            last_update=last_update
        )
        contact.save()
        obj = Contact.objects.all()
        for i in obj:
            print("datas : ",i.message, i.name)

        return redirect('ad_home')  # Redirect to a success page after form submission

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contact/contact_list.html', {'contacts': contacts})