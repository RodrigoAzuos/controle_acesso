from django import forms
from .models import Visitante, Veiculo, Endereco, Pessoa, RegistroAcesso
from django.forms.models import inlineformset_factory

class PessoaForm(forms.ModelForm):

  class Meta:
    model = Pessoa
    fields = '__all__'
    widgets = {
      'cpf': forms.NumberInput(
        attrs = {
          'class': 'form-control'
        }
      ),
      'telefone': forms.NumberInput(
        attrs = {
          'class': 'form-control'
        }
      ),
      'genero': forms.Select(
        attrs = {
          'class': 'form-control'
        }
      ),
      'data_nascimento': forms.DateInput(
        attrs = {
          'class': 'form-control'
        }
      ),
    }

class VisitanteForm(forms.ModelForm):

  class Meta:
    model = Visitante
    fields = '__all__'
    widgets = {
      'tipo': forms.Select(
        attrs = {
          'class': 'form-control'
        }
      ),
      'nome': forms.TextInput(
        attrs = {
          'class': 'form-control'
        }
      ),
      'cpf': forms.NumberInput(
        attrs = {
          'class': 'form-control'
        }
      ),
      'telefone': forms.NumberInput(
        attrs = {
          'class': 'form-control'
        }
      ),
      'genero': forms.Select(
        attrs = {
          'class': 'form-control'
        }
      ),
      'data_nascimento': forms.DateInput(
        attrs = {
          'class': 'form-control'
        }
      ),
    }

class VeiculoForm(forms.ModelForm):

  class Meta:
    model = Veiculo
    # fields = '__all__'
    exclude = ('pessoa',)
    widgets = {
      'placa': forms.TextInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      'modelo': forms.TextInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      'ano': forms.TextInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      'cor': forms.TextInput(
        attrs= {
          'class': 'form-control'
        }
      ),
    }

class EnderecoForm(forms.ModelForm):

  class Meta:
    model = Endereco
    # fields = '__all__'
    exclude = ('pessoa',)
    widgets = {
      'logradouro': forms.TextInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      'numero': forms.NumberInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      'bairro': forms.TextInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      'cidade': forms.TextInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      'estado': forms.TextInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      'cep': forms.NumberInput(
        attrs= {
          'class': 'form-control'
        }
      ),
      
    }

class RegistroAcessorForm(forms.ModelForm):
  class Meta:
    model = RegistroAcesso
    # fields = '__all__'
    exclude = ('status', 'data_hora_saida','data_hora_entrada')

    widgets = {
      'pessoa': forms.Select(
        attrs= {
          'class': 'form-control'
        }
      ),
      'veiculo': forms.Select(
        attrs= {
          'class': 'form-control'
        }
      ),
      'data_hora_entrada': forms.DateTimeInput(
        attrs= {
          'class': 'form-control'
        }
      ),
    }


