# views.py
from django.shortcuts import render, get_object_or_404, redirect
from base.models import Config


def config_list(request, path):
    configs = Config.objects.filter(q_path=path)
    return render(request, 'TimeConfig/config_list.html', {'configs': configs,'path':path})

def create_config(request, path):
    try:
        # Attempt to get the latest configuration for the given path
        obj = Config.objects.filter(q_path=path).latest('updated_date')
        configs = Config.objects.filter(q_path=path)
        return render(request, 'TimeConfig/Show_msg.html', {'configs': configs, 'path': path, 'obj': obj})
    except Config.DoesNotExist:
        # If no configuration found, handle the exception and proceed to create a new configuration
        try:
            if request.method == 'POST':
                time_mis = request.POST.get('time_mis', '')
                Config.objects.create(q_path=path, time_mis=time_mis)
                return redirect('create_config', path=path)
                
            return render(request, 'TimeConfig/create_config.html', {'path': path})
        except Exception as e:
            print("error", e)
            # Handle any other exceptions if necessary
            return render(request, 'TimeConfig/error.html', {'error_message': 'An error occurred'})

def update_config(request, config_id, path):
    config = get_object_or_404(Config, pk=config_id)

    if request.method == 'POST':
        time_mis = request.POST.get('time_mis', '')
        config.time_mis = time_mis
        config.save()
        return redirect('list_folders', path)

    return render(request, 'TimeConfig/update_config.html', {'config': config, "path":path})

def delete_config(request, config_id,path):
    config = get_object_or_404(Config, pk=config_id)
    config.delete()
    return redirect('config_list',path)
