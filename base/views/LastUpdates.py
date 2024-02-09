from django.shortcuts import render, redirect
from base.models import LatestUpdate

def latest_update_list(request):
    updates = LatestUpdate.objects.all()[::-1]
    if request.user.is_superuser:
        return render(request, 'LastUpdates/latest_update_list.html', {'updates': updates})
    else:
        return render(request, 'UserView/admin_error.html')

def create_latest_update(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        LatestUpdate.objects.create(message=message)
        return redirect('latest_update_list')
    if request.user.is_superuser:
        return render(request, 'LastUpdates/create_latest_update.html')
    else:
        return render(request, 'UserView/admin_error.html')

def delete_latest_update(request, pk):
    update = LatestUpdate.objects.get(pk=pk)
    update.delete()
    return redirect('latest_update_list')
