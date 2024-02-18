# views.py

from django.http import HttpResponse
from django.conf import settings
import os

def serve_ads_txt(request):
    ads_txt_path = os.path.join(settings.STATIC_ROOT, 'ads.txt')
    with open(ads_txt_path, 'r') as f:
        ads_txt_content = f.read()
    return HttpResponse(ads_txt_content, content_type='text/plain')
