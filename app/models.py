from django.db import models
from mptt.models import MPTTModel, TreeForeignKey



class Employee(MPTTModel):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    date = models.DateField()
    email = models.EmailField()
    manager = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subordinates')
    
    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'manager'