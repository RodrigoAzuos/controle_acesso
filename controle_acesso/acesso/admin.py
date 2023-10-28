from django.contrib import admin
from .models import Funcionario

# Register your models here.

class FuncionarioAdmin(admin.ModelAdmin):
  pass

admin.site.register(Funcionario, FuncionarioAdmin)