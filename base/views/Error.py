from django.shortcuts import render, redirect


def custom_404(request, exception):
    return render(request, 'home/page-404.html', status=404)
def custom_500(request):
    # Your custom error handling logic here
    if not request.user.is_authenticated:
        # User is logged in
        return redirect("login")
    else:
        return render(request, 'home/page-500.html', status=500)
def custom_403(request, exception):
    if not request.user.is_authenticated:
        # User is logged in
        return redirect("login")
    else:
        return render(request, 'home/page-403.html', status=404)

