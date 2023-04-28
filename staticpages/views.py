from django.shortcuts import render, redirect, get_object_or_404
from .models import DailyUpdate
from .forms import UpdateForm
from django.contrib.auth.decorators import login_required
from datetime import timezone, timedelta
import datetime
from django.utils import timezone
from django.core.cache import cache


def home(request):
    return render(request,'index.html')

@login_required
def update(request):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    urname = DailyUpdate.objects.filter(date__date=today)
    return render(request, 'updatenodu.html', {'urname':urname})
        
@login_required
def pleaseupdate(request):
    today = datetime.date.today()
    cache_key = f'my_form_submitted_{request.user.id}_{today.isoformat()}'

    if cache.get(cache_key):
        return redirect('formsubmitted')

    if request.method == 'GET':
        return render(request, 'updatemadu.html', {'form': UpdateForm()})
    else:
        try:
            form = UpdateForm(request.POST)
            newUpdate = form.save(commit=False)
            newUpdate.user = request.user
            newUpdate.save()
            cache.set(cache_key, True, 86400)
            return redirect('index')
        except ValueError:
            return render(request, 'updatemadu.html', {'form':UpdateForm(), 'error': 'Idiot, you just passed in bad data'})

@login_required            
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def formsubmitted(request):
    return render(request, 'formsubmitted.html')

@login_required
def updatecomment(request, id):
    obj = get_object_or_404(DailyUpdate, id=id)
    form = UpdateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'updateactivity.html', {'form':form, 'obj':obj})
