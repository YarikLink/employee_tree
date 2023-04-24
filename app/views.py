from django.shortcuts import render
from datetime import date as dt
from app.models import Employee
from app.forms import EmployeeForm
from mptt.templatetags.mptt_tags import cache_tree_children
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from pprint import pprint




class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employee_list.html'
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            if sort_by.startswith('-'):
                queryset = queryset.order_by(F(sort_by[1:]).desc(nulls_last=True))
            else:
                queryset = queryset.order_by(F(sort_by).asc(nulls_last=True))
        return queryset



class EmployeeCreate(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'employee_create.html'
    fields = ['name', 'position', 'date', 'email', 'manager']
    success_url = reverse_lazy('index')
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        managers = Employee.objects.select_related('manager').all()
        context['managers'] = managers
        return context

    
class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'employee_edit.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    login_url = '/login/'


class EmployeeDelete(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'employee_edit.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    login_url = '/login/'


@login_required(login_url='login')
def employee_delete(request, pk):
    Employee.objects.get(pk=pk).delete()
    return redirect(reverse('employee_list'))


@login_required(login_url='login')
def index(request):
    nodes = Employee.objects.all()
    return render(request, 'index.html', {'nodes': nodes})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('login')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')