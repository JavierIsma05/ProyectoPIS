from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .choices import *
# Create your models here.

#TUTORIAS
class Tutoria(models.Model):
    date = models.DateField('Fecha Tutoria',blank=False,null=False)
    description = models.TextField(blank=True,null=True,verbose_name='Tema Tratado')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'profesores'}, verbose_name='Profesor')
    status = models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], max_length=10, default='pending')
    time_quantity = models.PositiveIntegerField(default=0,verbose_name='Tiempo Empleado')
    modalidad = models.CharField(max_length=10,verbose_name='Modalidad',choices=modalidad, default='P')
    firma = models.ImageField(default='default.png', upload_to='firmas/',verbose_name='Firma')

    def __str__(self):
        return str(self.date) 
    
    class Meta:
        verbose_name = 'Tutoria'
        verbose_name_plural = 'Tutorias'

#INSCRIPCIOINES
class Registration(models.Model):
    tuto = models.ForeignKey(Tutoria, on_delete=models.CASCADE,verbose_name='Fecha')
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='students_registration', limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiante')
    enabled = models.BooleanField(default=True,verbose_name='Alumno Regular')
    
    
    def __str__(self):
        return f'{self.student.username} - {self.tuto.description}'

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones' 

#ASISTENCIAS
class Attendance(models.Model):
    tuto = models.ForeignKey(Tutoria, on_delete=models.CASCADE,verbose_name='Tutoria')
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='attendance', limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiante')
    present = models.BooleanField(default=False,blank=True,null=True,verbose_name='Presente')
    
    def __str__(self):
        return f'Asistencia {self.id}'
    # logica para generar el estado del alumno regular / irregular 
    # total-clases => class.quantity del modelo Tuto
    # to
    # porce
    # total-tutos
    # total--assistencias
    # porcentaje-inasistencias

    def update_registration_enabled_status(self):
        tuto_instance = Tutoria.objects.get(id=self.tuto.id)
        total_tutos = tuto_instance.time_quantity
        total_absences = Attendance.objects.filter(student=self.student, tuto= self.tuto, present=False).count()
        absences_percent = (total_absences / total_tutos)*100
        registration = Registration.objects.get(tuto=self.tuto, student=self.student)

        if absences_percent > 20:
            registration.enabled = False
        else:
            registration.enabled = True
        registration.save()


    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias' 

# NOTAS
class Mark(models.Model):
    tuto = models.ForeignKey(Tutoria,on_delete=models.CASCADE, verbose_name='Tutoria')
    student = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'groups__name':'estudiantes'},verbose_name='Estudiante')
    mark_1 = models.DecimalField(max_digits=3,decimal_places=2,null=True,blank=True,verbose_name='Nota 1')
    mark_2 = models.DecimalField(max_digits=3,decimal_places=2,null=True,blank=True,verbose_name='Nota 2')
    mark_3 = models.DecimalField(max_digits=3,decimal_places=2,null=True,blank=True,verbose_name='Nota 3')
    average = models.DecimalField(max_digits=3,decimal_places=2,null=True,blank=True,verbose_name='Promedio')

    def __str__(self):
        return str(self.tuto)
    
    #calcular el promedio
    def calculate_average(self):
        marks = [self.mark_1,self.mark_2,self.mark_3]
        valid_marks = [mark for mark in marks if mark is not None]
        if valid_marks:
            return sum(valid_marks) / len(valid_marks)
        return None
    
    def save(self, *args,**kwargs):
        # Version si alguna nota cambia
        if(self.mark_1 or self.mark_2 or self.mark_3):
            self.average = self.calculate_average()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'


@receiver(post_save, sender = Attendance)
@receiver(post_delete,sender = Attendance)
def update_registration_enabled_status(sender,instance,**kwargs):
    instance.update_registration_enabled_status()