from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # PAGINA DE INICIO
    path('', HomeView.as_view(), name='home'),

    # PAGINA DE PRECIOS
    path('pricing/', PricingView.as_view(), name='pricing'),

    # PAGINA DE LOGIN Y REGISTRO
    path('register/',RegisterView.as_view(),name='register'),

    # PAGINA DE PERFIL
    path('profile/', login_required(ProfileView.as_view()), name='profile'),

    # PAGINA DE TUTORIAS
    path('tutorias/',login_required(TutoriasView.as_view()),name='tutorias'),
    
    # PAGINA SOLICITAR TUTORIA
    path('tutorias/create',login_required(TutoriaSolicitarView.as_view()),name='tutorias_create'),
    
    #PAGINA EDITAR TUTORIA
    path('tutorias/<int:pk>/edit/',login_required(TutoriaEditarView.as_view()),name='tutorias_edit'),
    # PAGINA DE EERORES
    path('error/',login_required(ErrorView.as_view()),name='error'),

    # Imprimir datos
    path('tutorias/invoice/pdf/<int:pk>/',TutoriaInvoicePdfView.as_view(),name='tutorias_invoice'),
    path('tutorias/aceptar/<int:request_id>/', accept_tutoring_request, name='accept_tutoring_request'),
    path('tutorias/cancelar/<int:request_id>/', deny_tutoring_request, name='deny_tutoring_request'),

    path('generar_pdf/', generate_pdf, name='generate_pdf'),
]