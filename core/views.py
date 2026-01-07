from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CreditApplicationForm
from .models import CreditApplication

def home(request):
    """Главная страница (лендинг)"""
    return render(request, 'home.html')

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def apply_credit(request):
    """Подача заявки на кредит (только для авторизованных)"""
    if request.method == 'POST':
        form = CreditApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # привязываем к текущему пользователю
            application.save()
            return redirect('home')
    else:
        form = CreditApplicationForm()
    return render(request, 'apply.html', {'form': form})

@login_required
def my_applications(request):
    """Страница с фильтрацией заявок пользователя по статусу"""
    status = request.GET.get('status')
    applications = CreditApplication.objects.filter(user=request.user)
    
    # Фильтрация по статусу, если указан
    if status and status in ['new', 'approved', 'rejected']:
        applications = applications.filter(status=status)
    
    return render(request, 'my_applications.html', {
        'applications': applications,
        'current_status': status
    })