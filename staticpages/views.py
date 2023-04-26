from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import DailyUpdate
from .forms import UpdateForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'index.html')

@login_required
def update(request):
    urname = DailyUpdate.objects.all()
    return render(request, 'updatenodu.html',{'urname':urname})

@login_required
def pleaseupdate(request):
    if request.method == 'GET':
        return render(request, 'updatemadu.html', {'form': UpdateForm()})
    else:
        try:
            form = UpdateForm(request.POST)
            newUpdate = form.save(commit=False)
            newUpdate.user = request.user
            newUpdate.save()
            return redirect('index')
        except ValueError:
            return render(request, 'updatemadu.html', {'form':UpdateForm(), 'error': 'Idiot, you just passed in bad data'})

@login_required            
def dashboard(request):
    return render(request, 'dashboard.html')