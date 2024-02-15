from django.shortcuts import render


def custom_404(request, exception):
    return render(request, 'home/page-404.html', status=404)
def custom_500(request):
    # Your custom error handling logic here
    return render(request, 'home/page-500.html', status=500)
def custom_403(request, exception):
    return render(request, 'home/page-403.html', status=404)

