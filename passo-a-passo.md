Crie um repositorio no seu github com o nome controle_acesso. Clone o repositorio para sua marquina, em sua maquina execute o seguinte comando:

```bash
git clone <url do seu repositorio>
```

Entre na pasta que você clonou:
```bash
cd controle_acesso
```

Estando dentro no diretorio clonado execute o seguinte comando para iniciar o projeto:

```bash
django-admin startproject controle_acesso
```

Com o projeto criado execute o seguinte comando para criar a aplicacao acesso:

```bash
python3 manage.py startapp acesso
```

Com a aplicacão criada adicione a nova aplicacao na lista de apps instalados no arquivo controle_acesso/settings.py assim como no exemplo abaixo:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'acesso',
]
```

Ainda neste arquivo altere a linguagem e a time zone do seu projeto, para que seja possivel o admin ficar em portugues e a time zone ser a do brasil:

```python
LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'
```

Execute o seguinte comando para Criar as tabelas comuns do django:

```bash
python3 manage.py migrate
```

Resultado esperado:

```bash
Operations to perform:
  Apply all migrations: acesso, admin, auth, contenttypes, sessions
Running migrations:
  Applying acesso.0001_initial... OK
```

Execute o servidor web para validar se está tudo Ok com a aplicação:
```bash
python3 manage.py runserver
```
Agora podemos criar os nossos modelos, no arquivo acesso/models.py crie os modelos semelhantes ao exemplificado abaixo:

```python
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Pessoa(models.Model):
  SEXO_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Feminino')
  )
  nome = models.CharField(max_length=256, blank=False, null=False)
  cpf = models.CharField(max_length=11, blank=False, null=False)
  telefone = models.CharField(max_length=11, blank=True, null=True)
  genero = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False, null=False)
  data_nascimento = models.DateField(blank=False, null=False)

  def __str__(self):
    return self.nome
  
class Funcionario(Pessoa):
  TURNO_CHOICES = (
    ('M', 'Manhã'),
    ('T', 'Tarde'),
    ('N', 'Noite'),
  )

  matricula = models.CharField(max_length=5, blank=False, null=False)
  cargo = models.CharField(max_length=256, blank=False, null=False)
  turno = models.CharField(max_length=1, choices=TURNO_CHOICES, blank=False, null=False)
  usuario = models.OneToOneField(User, related_name= 'funcionario', on_delete=models.CASCADE)

class Visitante(Pessoa):
  TIPO_CHOICES = (
    ('E', 'Escola'),
    ('D', 'Delivery'),
    ('V', 'Visita técnica'),
  )

  tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, blank=False, null=False)

class Endereco(models.Model):
  logradouro = models.CharField(max_length=256, blank=False, null=False)
  numero = models.CharField(max_length=8, blank=True, null=True)
  bairro = models.CharField(max_length=256, blank=False, null=False)
  cidade = models.CharField(max_length=256, blank=False, null=False)
  estado = models.CharField(max_length=256, blank=False, null=False)
  cep = models.CharField(max_length=8, blank=False, null=False)
  pessoa = models.ForeignKey(Pessoa, blank=False, null=False, on_delete=models.CASCADE, related_name='enderecos')

class Veiculo(models.Model):
  placa = models.CharField(max_length=12, blank=False, null=False)
  modelo = models.CharField(max_length=64, blank=False, null=False)
  ano = models.IntegerField(null=False, blank=False)
  cor = models.CharField(max_length=64, blank=False, null=False)
  pessoa = models.ForeignKey(Pessoa, blank=False, null=False, on_delete=models.CASCADE, related_name='veiculos')

  def __str__(self):
    return self.placa + " de " + self.pessoa.nome

class RegistroAcesso(models.Model):
  STATUS_CHOICES = (
    ('E', 'Em andamento'),
    ('F', 'Finalizado'),
  )
  pessoa = models.ForeignKey(Pessoa, blank=False, null=False, on_delete=models.CASCADE)
  veiculo = models.ForeignKey(Veiculo, blank=True, null=True, on_delete=models.CASCADE)
  data_hora_entrada = models.DateTimeField(blank=False, null=False)
  data_hora_saida = models.DateTimeField(blank=True, null=True)
  status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='E', blank=False, null=False)

  def atualiza_status(self):
    self.status = 'F'
    self.atualiza_hora_saida(datetime.now())
    self.save()

  def atualiza_hora_saida(self, hora_saida):
    self.data_hora_saida = hora_saida
    self.save()
```

No exemplo acima, note os imports que foram feitos.


Tendo criado os modelos execute o seguinte comando para criar as migracoes dos modelos criados:

```bash
python3 manage.py makemigrations
```

Resultado esperado:

```bash
acesso/migrations/0001_initial.py
    - Create model Pessoa
    - Create model Funcionario
    - Create model Visitante
    - Create model Veiculo
    - Create model RegistroAcessor
    - Create model Endereco
```

Execute o seguinte comando para aplicar a criacao de tabelas a partir dos modelos criados
```bash
python3 manage.py migrate
```

Crie o diretorio/pasta templates dentro da aplicacao acesso: No caso da aplicacao esta dividido por escopo, portanto dentro deste diretorio deve ser criado dois outros diretorios o acesso e visitante.

Comece criando o template base.html neste arquivo terá configuracões bases do projeto como importacao do bootstrap e do arquivo css que iremos criar.

```html
{% load static %}

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
	<link rel="stylesheet" href="{% static 'acesso/base.css' %}">
	<title>{% block title %}{% endblock %}</title>
</head>
<body>
	<div class="container">
		<ul class="nav nav-pills">
			<li class="nav-item">
		    <a class="nav-link" href="{% url 'index' %}">Inicio</a>
		  </li>
		  <li class="nav-item">
		    <a class="nav-link" href="{% url 'visitantes' %}">Visitantes</a>
		  </li>
		  <li class="nav-item">
		    <a class="nav-link"  href="{% url 'registrar_acesso' %}">Registrar acesso</a>
		  </li>
		</ul>
		{% block content %}
			
		{% endblock %}
	</div>
	<!-- Latest compiled and minified JavaScript -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>
</body>
</html>
```
### Note:

Os scrips copiados no header e na parte final do projeto como:

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" 

<!-- Latest compiled and minified JavaScript -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>
```

Servem para adicionar bootstrap ao projetos, para acessar a documentacao do bootstrap acesse o seguinte site <https://getbootstrap.com/docs/5.3/getting-started/introduction/> está sendo utilizando o bootstrap 5.3.

Note tambem que a aplicação está carregando um arquivo próprio de css, para criar a estrutura de arquivos css, crie um diretorio/pasta chamada static dentro do diretorio da aplicacao acesso, semelhante ao que foi feito com o diretorio templates. Destro deste diretorio crie um outro diretorio chamado acesso, pois por padrão é aqui que os arquivos css serão procurados. E em seguida crie um arquivo chamado base.css.

Assim o uso do css feito no arquivo base.html poderá ser importado:

```html
<link rel="stylesheet" href="{% static 'acesso/base.css' %}">
```

O arquivo base.css criado no diretorio acesso/static/acesso/base.css tem o seguinte conteudo:

```css
h2 {
  color: rgb(70, 78, 70);
}

h3 {
  color: rgb(141, 143, 140);
}

.card {
  margin-bottom: 2rem;
}

div.row-login{
  position: relative;
  width: 100%;
}

div.login {
  left: 50%;
  position: absolute;
  transform: translateX(-50%);
  text-align: center;
}

#id_username, #id_password {
  width: 90%; 
}
```

Em templates crie o arquivo index.html:

```html
{% extends "base.html" %}

{% block content %}
	<h2>Visitantes</h2>
  <a class="btn btn-sm btn-primary" href="{% url 'novo_visitante' %}">Novo visitante</a>

  <h3>Listagem de visitantes</h3>

  <table class="table">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Nome</th>
        <th scope="col">Veículo</th>
        <th scope="col">Data entrada</th>
				<th scope="col">Hora saída</th>
        <th scope="col">Status</th>
				<th scope="col">Ação</th>
      </tr>
    </thead>
    <tbody>
      {% for acesso in acessos %}
        <tr>
          <th scope="row">{{acesso.id}}</th>
          <td>{{ acesso.pessoa.nome}}</td>
          <td>{{ acesso.veiculo}}</td>
          <td>{{ acesso.data_hora_entrada}}</td>
					{% if acesso.data_hora_saida %}
						<td>{{ acesso.data_hora_saida}}</td>
					{%else%}
						<td>-</td>
					{% endif %}
					{% if acesso.status == 'E' %}
						<span class="badge text-bg-warning"><td>{{ acesso.get_status_display}}</td></span>
					{%else%}
						<span class="badge text-bg-success"><td>{{ acesso.get_status_display}}</td></span>
					{% endif %}
          {% if acesso.status == 'E' %}
						<td><a href="{% url 'finalizar_acesso' acesso.id %}" class="btn btn-sm btn-success">Finalizar</a></td>
					{%else%}
						<td>-</td>
					{% endif %}
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

Se não criou ainda, crie um diretorio/pasta dentro de templates chamado visitante dentro dele serão criados quatro arquivos:

`index.html`

```html
{% extends "base.html" %}

{% block content %}
	<h2>Visitantes</h2>
  <a class="btn btn-sm btn-primary" href="{% url 'novo_visitante' %}">Novo visitante</a>

  <h3>Listagem de visitantes</h3>

  <table class="table">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Nome</th>
        <th scope="col">Telefone</th>
        <th scope="col">Data nascimento</th>
        <th scope="col">Acão</th>
      </tr>
    </thead>
    <tbody>
      {% for visitante in visitantes %}
        <tr>
          <th scope="row">{{visitante.id}}</th>
          <td>{{ visitante.nome}}</td>
          <td>{{ visitante.telefone}}</td>
          <td>{{ visitante.data_nascimento}}</td>
          <td><a href="{% url 'visitante' visitante.id %}" class="btn btn-sm btn-secondary">Visualizar</a></td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

`new.html`
```html
{% extends "base.html" %}

{% block content %}
	<h2>Criar Visitante</h2>
  <form method="POST" enctype="multipart/form-data">
 
    <!-- Security token -->
    {% csrf_token %}
    
    
    <div class="card">
      <div class="card-body">
        <div class="card-title">
          <h3>Dados visitante</h3>
        </div>
        
        {% if form_visitante.errors %}
          <div class="alert alert-danger">
            <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">
            </button>
            por favor, verifique erros
            {{ form_visitante.errors }}
          </div>
        {% endif %}
        {{form_visitante}}
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="card-title">
          <h3>Dados endereco</h3>
        </div>
        {% if form_endereco.errors %}
          <div class="alert alert-danger">
            <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">
            </button>
            por favor, verifique erros
            {{ form_endereco.errors }}
          </div>
        {% endif %}
        {{form_endereco}}

      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <div class="card-title">
          <h3>Dados Veículo</h3>
        </div>
        {% if form_veiculo.errors %}
          <div class="alert alert-danger">
            <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">
            </button>
            por favor, verifique erros
            {{ form_veiculo.errors }}
          </div>
        {% endif %}
        {{form_veiculo}}
      </div>
      <div class="card-footer">
        <input type="submit" value="Salvar" class="btn btn-sm btn-primary">
        <a href="{% url 'index' %}" class="btn btn-sm btn-secondary">Voltar</a>
      </div>
    </div>
  </form>
{% endblock %}
```

`view.html`
```html
{% extends "base.html" %}

{% block content %}
	<h2>Visitante</h2>

  <div class="row">
    <div class="col-6">
      <div class="card">
        <div class="card-body">
          <div class="card-title">
            <h3>Dados do visitante</h3>
          </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item"><dt>Nome</dt><dd>{{visitante.nome}}</dd></li>
              <li class="list-group-item"><dt>cpf</dt><dd>{{visitante.cpf}}</dd></li>
              <li class="list-group-item"><dt>Telefone</dt><dd>{{visitante.telefone}}</dd></li>
              <li class="list-group-item"><dt>Genero</dt><dd>{{visitante.get_genero_display}}</dd></li>
              <li class="list-group-item"><dt>Data nascimento</dt><dd>{{visitante.data_nascimento}}</dd></li>
              <li class="list-group-item"><dt>Tipo</dt><dd>{{visitante.get_tipo_display}}</dd></li>
              <li class="list-group-item"><a href="{% url 'editar_visitante' visitante.id %}" class="btn btn-sm btn-primary">Editar</a></li>
            </ul>
        </div>
      </div>
    </div>
  
    <div class="col-6">
      <div class="card">
        <div class="card-body">
          <div class="card-title">
            <h3>Endereço</h3>
          </div>
            {% for endereco in visitante.enderecos.all %}  
              <ul class="list-group list-group-flush">
                <li class="list-group-item"><dt>Logradouro</dt><dd>{{endereco.logradouro}}</dd></li>
                <li class="list-group-item"><dt>Numero</dt><dd>{{endereco.numero}}</dd></li>
                <li class="list-group-item"><dt>Bairro</dt><dd>{{endereco.bairro}}</dd></li>
                <li class="list-group-item"><dt>Cidade</dt><dd>{{endereco.cidade}} - {{endereco.estado}}</dd></li>
                <li class="list-group-item"><dt>Cep</dt><dd>{{endereco.cep}}</dd></li>
                <li class="list-group-item"><a href="#" class="btn btn-sm btn-primary">Editar</a></li>
              </ul>
            {%endfor%}
        </div>
      </div>
    </div>
  </div>
  
  <div class="row-fluid">
    <div class="card">
      <div class="card-body">
        <div class="card-title">
          <h3>Veículos</h3>
        </div>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Placa</th>
              <th scope="col">Cor</th>
              <th scope="col">modelo</th>
            </tr>
          </thead>
          <tbody>
            {% for veiculo in visitante.veiculos.all %}
              <tr>
                <th scope="row">{{veiculo.placa}}</th>
                <td>{{ veiculo.modelo}}</td>
                <td>{{ veiculo.cor}}</td>
                <td><a href="#" class="btn btn-sm btn-primary">Editar</a></td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
{% endblock %}
```

`edit.html`

```html
{% extends "base.html" %}

{% block content %}
	<h2>Editar Visitante</h2>
  <form method="POST" enctype="multipart/form-data">
 
    <!-- Security token -->
    {% csrf_token %}
    
    
    <div class="card">
      <div class="card-body">
        <div class="card-title">
          <h3>Dados visitante</h3>
        </div>
        
        {% if form_visitante.errors %}
          <div class="alert alert-danger">
            <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">
            </button>
            por favor, verifique erros
            {{ form_visitante.errors }}
          </div>
        {% endif %}
        {{form_visitante}}
      </div>
      <div class="card-footer">
        <input type="submit" value="Salvar" class="btn btn-sm btn-primary">
        <a href="{% url 'visitante' visitante.id %}" class="btn btn-sm btn-secondary">Voltar</a>
      </div>
    </div>
  </form>
{% endblock %}
```

Se não criado ainda, crie o diretorio/pasta chamado acesso, nele será criado o diretorio relacionado ao registro de acesso.

Dentro deste dieretorio será criado o arquivo registrar.html:

`registrar.html`

```html
{% extends "base.html" %}

{% block content %}
	<h2>Registrar acesso</h2>
  <form method="POST" enctype="multipart/form-data">
 
    <!-- Security token -->
    {% csrf_token %}
    
    
    <div class="card">
      <div class="card-body">
        <div class="card-title">
          <h3>Acesso</h3>
        </div>
        
        {% if form.errors %}
          <div class="alert alert-danger">
            <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">
            </button>
            por favor, verifique erros
            {{ form.errors }}
          </div>
        {% endif %}
        {{form}}
      </div>
      <div class="card-footer">
        <input type="submit" value="Registrar" class="btn btn-sm btn-success">
        <a href="{% url 'index' %}" class="btn btn-sm btn-secondary">Voltar</a>
      </div>
    </div>
  </form>
{% endblock %}
```
Para que seja possivel criar os objetos a partir dos templates é necessário que sejam criados os fomularios, para isso crie dentro do diretorio da aplicação acesso um arquivo chamado forms.py com o conteudo abaixo:

`acesso/forms.py`

```python
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
```

Coms os templates criados agora é hora de criar as views relacionadas aos templates, no arquivo views.py presente no diretorio da aplicacao acesso adicione o seguinte conteudo:

`acesso/views.py`

```python
from django.shortcuts import render, redirect
from .models import RegistroAcesso, Visitante
from .forms import EnderecoForm, VeiculoForm, VisitanteForm, RegistroAcessorForm
from django.shortcuts import get_object_or_404
from datetime import datetime

def index(request):
  acessos = RegistroAcesso.objects.all()
  context = { "acessos": acessos }
  return render(request, 'index.html', context)

def visitantes(request):
  visitantes = Visitante.objects.all()
  context = { "visitantes": visitantes}
  return render(request, 'visitante/index.html', context)

def novo_visitante(request):
  form_endereco = EnderecoForm()
  form_visitante = VisitanteForm()
  form_veiculo = VeiculoForm()

  if request.method == 'POST':
    form_endereco = EnderecoForm(request.POST)
    form_visitante = VisitanteForm(request.POST)
    form_veiculo = VeiculoForm(request.POST)
    
    if form_visitante.is_valid() and form_endereco.is_valid() and form_veiculo.is_valid:
      visitante = form_visitante.save()
      endereco = form_endereco.save(commit=False)
      veiculo = form_veiculo.save(commit=False)
      veiculo.pessoa = visitante
      veiculo.save()
      endereco.pessoa = visitante
      endereco.save()

  context = { "form_endereco": form_endereco, "form_visitante": form_visitante, "form_veiculo": form_veiculo}
  return render(request, 'visitante/new.html', context)

def visitante(request, visitante_id):
  visitante = get_object_or_404(Visitante, id=visitante_id)
  context = { "visitante": visitante }
  return render(request, 'visitante/view.html', context)

def editar_visitante(request, visitante_id):
  visitante = get_object_or_404(Visitante, id=visitante_id)
  form_visitante = VisitanteForm(instance=visitante)
  

  if request.method == 'POST':
    form_visitante = VisitanteForm(request.POST, instance=visitante)
  
    if form_visitante.is_valid():
      form_visitante.save()
      return redirect('visitante', visitante.id)

  context = { "visitante": visitante, "form_visitante": form_visitante }

  return render(request, 'visitante/edit.html', context)

def registrar_acesso(request):
  form = RegistroAcessorForm()

  if request.method == 'POST':
    form = RegistroAcessorForm(request.POST)

    if form.is_valid():
      datetime.now()
      acesso = form.save(commit=False)
      acesso.data_hora_entrada = datetime.now()
      acesso.save()
      return redirect('index')
  
  context = { "form": form }

  return render(request, 'acesso/registrar.html', context)

def finalizar_acesso(request, acesso_id):
  acesso = get_object_or_404(RegistroAcesso, id=acesso_id)
  acesso.atualiza_status()
  return redirect(index)
```

Com as viewn criadas,agora é possivel criar as urls da aplicacao, para isso dentro do diretorio acesso crie um arquivo chamado urls.py com o seguinte conteudo:

```python
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('visitantes/', views.visitantes, name='visitantes'),
  path('novo-visitante/', views.novo_visitante, name='novo_visitante'),
  path('visitante/<int:visitante_id>/', views.visitante, name='visitante'),
  path('visitante/editar/<int:visitante_id>/', views.editar_visitante, name='editar_visitante'),

  path('registrar-acesso/', views.registrar_acesso, name='registrar_acesso'),
  path('finalizar-acesso/<int:acesso_id>/', views.finalizar_acesso, name='finalizar_acesso'),
]
```

Para que seja possivel a utilização é necessario importar o arquivo nas urls pradões da aplicacão para isso deixe o arquivo `controle_acesso/urls.py` como o exemplo abaixo:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('acesso.urls')),
]
```

> Note: neste arquivo será importado todos os arquivos de urls de aplicacoes que podem vir a existir.


Os funcionarios serão criados na aplicacão por meio do admin do django para isso registre Funcionario no site admin. Abra o arquivo `acesso/admin.py` e deixe-o assim como no exemplo abaixo:

```python
from django.contrib import admin
from .models import Funcionario

# Register your models here.

class FuncionarioAdmin(admin.ModelAdmin):
  pass

admin.site.register(Funcionario, FuncionarioAdmin)
```
Com isso será possivel criar novos funcionários acessando a area administrativa do django: localhost:8000/admin

Para acessar a area administrativa é necessário a criação de super usuario, para isso execute o seguinte comando:

```bash
python manage.py createsuperuser
```


> Lembre-se de sempre manter o servidor de desenvolvimento rodando, para isso execute o seguinte comando: `python manage.py runserver`

# Adicionando projeto ao git:

```bash
git add .
```

```bash
git commit -m "criacao inicial de projeto"
```

```bash
git push
```

# Atualizando projeto em outra maquina

Já tendo feito o clone:

```bash
git clone <url do projeto>
```

Para atualizar na sua maquina local execute:

```bash
git pull
```

Sempre que criar coisas novas repita os passos do `add` ao `push`.  


### Adicionando autenticação simples

Crie templates para login, para isso crie um diretorio chamado registration dentro de acesso/templates:

Dentro de registration crie um arquivo chamado `login.html`
```html
{% extends "base_login.html" %}

{% block content %}

{% if form.errors %}
<div class="alert alert-danger">
    <button type="button" class="close" data-dismiss="alert"
    aria-hidden="true">
    </button>
    <p>Seu usuario e senha podem está incorretos. Tente novamente</p>
</div>
{% endif %}

{% if next %}
    {% if user.is_authenticated %}
    <div class="alert alert-danger">
        <button type="button" class="close" data-dismiss="alert"
        aria-hidden="true">
        </button>
        <p>Vocês não tem acesso a essa pagina, autentique-se para conseguir vê-la.</p>
    </div>
    {% else %}
    <div class="alert alert-warning">
        <p>Por favor, faça login aqui.</p>
    </div>
    {% endif %}
{% endif %}
<div class="row row-login">
  <div class="col-6 login">
    <div class="card">
      <div class="card-body"> 
        <form method="post" action="{% url 'login' %}">
          {% csrf_token %}
            <div class="form-group">
                <label for="{{ form.username.id_for_label }}">
                    {{ form.username.label_tag }}
                </label>
                <div class="form-group">
                    {{ form.username }}
                </div>
            </div>
            
            <div class="form-group">
                <label for="{{ form.password.id_for_label }}">
                {{ form.password.label_tag }}
                </label>
                <div class="form-group">
                    {{ form.password }}
                </div>
            </div>
        <br/>
        <input type="submit" value="login" class="btn btn-primary">
        <input type="hidden" name="next" value="{{ next }}">
        </form>
        
        <p><a href="{% url 'password_reset' %}">Esqueceu a senha?</a></p>
      </div>
    </div>
  </div>
</div>

{% endblock %}
```

Em templates crie um arquivo chamado base_login.html com o seguinte conteudo:

```html
{% load static %}

<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <link rel="stylesheet" href="{% static 'acesso/base.css' %}">
    <title>Login</title>
  </head>
  <body>
    <div class="container">
      {% block content %}
			
		  {% endblock %}
    </div>

    

    <!-- Latest compiled and minified JavaScript -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>
  </body>
</html>
```

Adicione o conteudo abaixo no arquivo `urls.py` da aplicação acesso:


```python
urlpatterns = [
  # codigo omitido
  path("contas/", include("django.contrib.auth.urls")),
]
```

Em acesso/views.py

Importe o sguinte decorator:

```python
from django.contrib.auth.decorators import login_required
```

Adicione o decorator sobre cada um dos metodos de views.py:

```python
@login_required(login_url="/contas/login/")
def index(request):
```

Exemplo de como deve ficar o arquivo views.py:

```python
from django.shortcuts import render, redirect
from .models import RegistroAcesso, Visitante
from .forms import EnderecoForm, VeiculoForm, VisitanteForm, RegistroAcessorForm
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url="/contas/login/")
def index(request):
  acessos = RegistroAcesso.objects.all()
  context = { "acessos": acessos }
  return render(request, 'index.html', context)
```


# Adicionando projeto ao git:

```bash
git add .
```

```bash
git commit -m "criacao inicial de projeto"
```

```bash
git push
```

# Atualizando projeto em outra maquina

Já tendo feito o clone:

```bash
git clone <url do projeto>
```

Para atualizar na sua maquina local execute:

```bash
git pull
```
