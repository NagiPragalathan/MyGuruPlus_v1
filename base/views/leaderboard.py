from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.contrib.auth.models import User
from django.shortcuts import render



from base.models import LeaderBoard

@csrf_exempt  # Only for demonstration, consider using proper CSRF protection in production
@require_POST
def update_leaderboard(request):
    try:
        data = json.loads(request.body)
        path = data.get('path')
        mark = data.get('mark')
        if path is None or mark is None:
            return {'status':"Both 'path' and 'mark' must be provided"}
        
        # Get the current user's leaderboard entry for the given path
        leaderboard_entry, created = LeaderBoard.objects.get_or_create(user_id=request.user, path=path)
        
        # If the entry already exists, update the mark and increment the attempt count
        if not created:
            leaderboard_entry.mark = mark
            leaderboard_entry.attempt += 1
        else:
            leaderboard_entry.mark = mark
            leaderboard_entry.attempt = 1  # Set attempt count to 1 for new entry
        
        leaderboard_entry.save()
        
        response_data = {'status': 'success', 'message': 'Data updated successfully'}
    except Exception as e:
        response_data = {'status': 'error', 'message': str(e)}

    return JsonResponse(response_data)

def leaderboard_view(request, path):
    # Filter leaderboard data based on the given path
    leaderboard_data = LeaderBoard.objects.filter(path=path).order_by('-mark')
    
    # Add ranking to the leaderboard data
    ranking = 1
    for entry in leaderboard_data:
        entry.rank = ranking
        ranking += 1

    # Get current user's data if available
    current_user_data = LeaderBoard.objects.filter(path=path, user_id=request.user).first()
    # Update current_user_data with rank
    if current_user_data:
        current_user_data.rank = leaderboard_data.filter(mark__gt=current_user_data.mark).count() + 1

    context = {
        'path': path,
        'leaderboard_data': leaderboard_data,
        'current_user_data': current_user_data
    }
    return render(request, 'leaderboard.html', context)