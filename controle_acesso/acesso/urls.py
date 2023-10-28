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
