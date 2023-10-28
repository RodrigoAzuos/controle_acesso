# controle_acesso
Aplicacão utilizada no aprendizado de alunos da linguagem python com django para construcão de aplicacões web. 

# Verificar versão do python instalada

```bash
$ python3 --version
$ sudo apt-get install python3
```

# Instalar PIP 

```bash
$ sudo apt-get install python3-pip
```

# Instalar virtualenv 

```bash
$ sudo apt install python3-venv
```

# Criando Virtualenv

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

# Instalando dependencias

```bash
$ pip install -r requirements.txt
```

# aplicando migracoes

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

# Iniciado aplicacão

```bash
$ python manage.py runserver
```