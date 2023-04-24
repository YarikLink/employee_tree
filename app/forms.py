from django.forms import ModelForm, Select, TextInput, EmailInput, DateInput
from app.models import Employee




class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'date', 'email', 'manager']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'position': TextInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'date': DateInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'email': EmailInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'manager': Select(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].queryset = Employee.objects.exclude(pk=self.instance.pk)
        self.fields['manager'].label_from_instance = lambda obj: obj.name