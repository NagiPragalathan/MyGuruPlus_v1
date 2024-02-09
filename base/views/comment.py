from django.shortcuts import render, redirect
from base.models import Comments, Rating
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required

def create_comment(request, path):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')  # Assuming comment is passed in the request
        if comment_text:
            user = request.user
            comment = Comments(user_id=user, comment=comment_text, category=path.split('.')[1])
            comment.save()
            return redirect('list_course', path=path)
        else:
            return HttpResponseNotFound("User ID and Comment are required.")
    else:
        return HttpResponseNotFound("Invalid request method.")

def update_comment(request, comment_id):
    try:
        comment = Comments.objects.get(pk=comment_id)
    except Comments.DoesNotExist:
        return HttpResponseNotFound("Comment does not exist.")

    if request.method == 'POST':
        comment_text = request.POST.get('comment')  # Assuming comment is passed in the request

        if comment_text:
            comment.comment = comment_text
            comment.save()
            return redirect('comment_list')  # Redirect to a view that lists all comments
        else:
            return HttpResponseNotFound("Comment is required.")
    else:
        return HttpResponseNotFound("Invalid request method.")

def delete_comment(request, comment_id):
    try:
        comment = Comments.objects.get(pk=comment_id)
    except Comments.DoesNotExist:
        return HttpResponseNotFound("Comment does not exist.")

    comment.delete()
    return redirect('comment_list')  # Redirect to a view that lists all comments

def comment_list(request):
    comments = Comments.objects.all()
    return render(request, 'comment_list.html', {'comments': comments})


@csrf_exempt
@login_required
def update_rating(request, path):
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        category = path.split('.')[1]
        user_id = request.user.id  # Get the ID of the current user

        try:
            # Check if the rating exists for the category and user
            rating = Rating.objects.get(category=category, user_id=user_id)
        except Rating.DoesNotExist:
            # If the rating doesn't exist, create a new one
            rating = Rating(category=category, user_id=user_id)

        # Update the rating value
        rating.rating = rating_value
        rating.save()

        # Calculate and return the updated average rating for the category
        average_rating = 0
        
        return JsonResponse({'average_rating': average_rating})

    return JsonResponse({'error': 'Invalid request'}, status=400)

