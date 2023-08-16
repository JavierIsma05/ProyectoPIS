from typing import Any, Dict, Optional
from django.forms.models import BaseModelForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.views.generic import TemplateView,CreateView,UpdateView,View
from django.contrib.auth.models import Group
from .forms import *
from django.views import View
from django.utils.decorators import method_decorator
from .models import *
from django.urls import reverse_lazy
from django.contrib import messages
from xhtml2pdf import pisa
from django.contrib.auth.mixins import UserPassesTestMixin
import os
from django.conf import settings
# DE IMPRESION
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

def plural_to_singular(plural):
    #Diccionario de palabras
    plural_singular = {
        "estudiantes":"estudiante",
        "profesores":"profesor",
        "decanos":"decano",
        "administrativos":"administrativo",
    }
    return plural_singular.get(plural,"error")

def add_group_name_to_context(view_class):
    original_dispatch = view_class.dispatch

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user 
        group = user.groups.first()
        group_name = None
        group_name_singular = None
        color = None
        if group:
            if group.name == 'estudiantes':
                color = 'bg-primary'
            elif group.name == 'profesores':
                color = 'bg-success'
            elif group.name == 'decanos':
                color = 'bg-secondary'
            elif group.name == 'administrativos':
                color = 'bg-danger'
            group_name = group.name
            group_name_singular = plural_to_singular(group.name)
        context = {
            'group_name': group_name,
            'group_name_singular': group_name_singular,
            'color': color
        }

        self.extra_context = context
        return original_dispatch(self,request,*args,**kwargs)
    view_class.dispatch = dispatch
    return view_class 
    

# PAGINA DE INICIO
@add_group_name_to_context
class HomeView(TemplateView):
    template_name = 'home.html'

# PAGINA DE PRECIOS
@add_group_name_to_context
class PricingView(TemplateView):
    template_name = 'pricing.html'

# REGISTRO DE USUARIOS
class RegisterView(View):
    def get(self,request):
        data = {
            'form': RegisterForm()
        }
        return render(request, 'registration/register.html',data)
    
    def post(self,request):
        user_creation_form = RegisterForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'],password=user_creation_form.cleaned_data['password1'])
            login(request,user)
            return redirect('home')
        data = {
            'form': user_creation_form
        }
        return render(request,'registration/register.html',data)

# PAGINA DE PREGUNTAS Y RESPUESTAS /ACERCA DE

# PAGINA DE LOGIN Y REGISTRO
# PAGINA DE PERFIL: VISTA DE PERFIL - EDICION DE PERFIL
@add_group_name_to_context
class ProfileView(TemplateView):
    template_name = 'profile/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_form'] = UserForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)
        return context
    
    def post(self,request,*args,**kwargs):
        user = self.request.user
        user_form = UserForm(request.POST,instance=user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # redireccionar a la pagina perfil (con datos actualizados)
            return redirect('profile')
        #si alguno de los datos no es valido
        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return render(request, 'profile/profile.html',context)

# PAGINA DE ADMINISTRACION LAS TUTORIAS
@add_group_name_to_context
class TutoriasView(TemplateView):
    template_name = 'tutorias.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tutorias = Tutoria.objects.all().order_by('-id')
        student = self.request.user if self.request.user.is_authenticated else None

        for item in tutorias:
            if student:
                registration = Registration.objects.filter(tuto=item,student=student).first()
                item.is_enrolled = registration is not None
            else:
                item.is_enrolled = False
            enrollment_count = Registration.objects.filter(tuto=item).count()
            item.enrollment_count = enrollment_count

        context['tutorias'] = tutorias
        return context

@add_group_name_to_context
class ErrorView(TemplateView):
    template_name = 'error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        error_image_path = os.path.join(settings.MEDIA_URL,'error.png')
        context['error_image_path'] = error_image_path
        return context
        

# PAGINA PARA SOLICITAR UNA TUTORIA
@add_group_name_to_context
class TutoriaSolicitarView(UserPassesTestMixin, CreateView):
    model = Tutoria
    form_class = TutoriaForm
    template_name = 'solicitar_tutoria.html'
    success_url = reverse_lazy('tutorias')
    
    def test_func(self):
        return self.request.user.groups.filter(name='estudiantes').exists()

    def handle_no_permission(self):
        return redirect('error')

    def form_valid(self,form):
        messages.success(self.request,'El registro se ha guardado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request, 'Ha ocurrido un error al guardar el registro')
        return self.render_to_response(self.get_context_data(form=form))
    
# EDITAR TUTORIA
@add_group_name_to_context
class TutoriaEditarView(UserPassesTestMixin, UpdateView):
    model = Tutoria
    form_class = TutoriaForm
    template_name = 'edit_tutoria.html'
    success_url = reverse_lazy('tutorias')

    def test_func(self):
        return self.request.user.groups.filter(name='estudiantes').exists()

    def handle_no_permission(self):
        return redirect('error')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,'El registro se actualizó correctamente')
        return redirect(self.success_url)
    
    def form_invalid(self,form):
        messages.error(self.request, 'Ha ocurrido un error al actualizar el registro')
        return self.render_to_response(self.get_context_data(form=form))
    
class TutoriaInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        template = get_template('pdf/invoice.html')
        context = {'title': 'UNIVERSIDAD NACIONA DE LOJA'}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="registroacademico.pdf"'
         # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)

        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')            
        return response

def accept_tutoring_request(request, request_id):
    if request.user.groups.filter(name='profesores').exists():
        tutoring_request = get_object_or_404(Tutoria, pk=request_id)
        tutoring_request.status = 'aceptada'
        tutoring_request.save()
    return redirect('tutorias')

def deny_tutoring_request(request, request_id):
    if request.user.groups.filter(name='profesores').exists():
        tutoring_request = get_object_or_404(Tutoria, pk=request_id)
        tutoring_request.status = 'cancelada'
        tutoring_request.save()
    return redirect('tutorias')

def generate_pdf(request):
        template = get_template('pdf/invoice.html')
        context = {'tutorias': Tutoria.objects.all()} 
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="registroacademico.pdf"'
         # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)

        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('Error al generar PDF', content_type='text/plain')           
        return response
    