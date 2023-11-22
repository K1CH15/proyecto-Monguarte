from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, make_password
from django.shortcuts import render, redirect

from usuario.forms import ComisionForm, ComisionUptadeForm
from usuario.forms import PersonaForm, PersonaUptadeForm
from usuario.models import Persona, Comision


# CRUD PERSONA

@login_required
def persona_crear(request):
    titulo = "Persona"
    mensaje = f'¡Hecho! Se ha añadido con éxito la {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'

    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            primer_nombre = form.cleaned_data['nombres'][0].upper()
            primer_apellido = form.cleaned_data['apellidos'][0].lower()
            ultimos_digitos_documento = form.cleaned_data['numero_documento'][-4:]
            nueva_contrasena = f"@{primer_nombre}{primer_apellido}{ultimos_digitos_documento}"
            contrasena_encriptada = make_password(nueva_contrasena)
            nuevo_usuario = User(
                username=form.cleaned_data['numero_documento'],
                password=contrasena_encriptada,
                email=form.cleaned_data['correo_electronico'],
                first_name=form.cleaned_data['nombres'],
                last_name=form.cleaned_data['apellidos']
            )
            nuevo_usuario.save()
            usuario = form.save(commit=False)
            usuario.persona = nuevo_usuario
            usuario.save()
            grupo_seleccionado = form.cleaned_data['rol']
            nuevo_usuario.groups.add(grupo_seleccionado)
            messages.success(request, mensaje)
            return redirect('personas')
        else:
            messages.error(request, mensajeerror)
    else:
        form = PersonaForm()
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "persona/crear.html", context)


@login_required
def persona_listar(request):
    titulo = "Persona"
    modulo = "usuarios"
    personas = Persona.objects.all()
    context = {
        "titulo": titulo,
        "modulo": modulo,
        "personas": personas,

    }
    return render(request, "persona/listar.html", context)


@login_required
def persona_modificar(request, pk):
    titulo = "Persona"
    mensaje = f'¡Hecho! La {titulo} se ha modificado exitosamente.'
    persona = Persona.objects.get(id=pk)
    if request.method == 'POST':
        form = PersonaUptadeForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('personas')
    else:
        form = PersonaUptadeForm(instance=persona)
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "persona/modificar.html", context)


@login_required
def persona_eliminar(request, pk):
    persona = Persona.objects.filter(id=pk)
    persona.update(
        estado="0"
    )

    return redirect('personas')


# CRUD Contabilidad

@login_required
def comision_crear(request):
    titulo = "Comisión"
    mensaje = f'¡Hecho! Se ha añadido con éxito la {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'
    if request.method == 'POST':
        form = ComisionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('comisiones')
        else:
            messages.error(request, mensajeerror)
    else:
        form = ComisionForm()
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "comision/crear.html", context)


@login_required
def comision_listar(request):
    titulo = "Comisión"
    modulo = "usuarios"
    comision = Comision.objects.all()
    context = {
        "titulo": titulo,
        "comisionesn": comision,
        "modulo": modulo,

    }
    return render(request, "comision/listar.html", context)


@login_required
def comision_modificar(request, pk):
    titulo = "Comisión"
    mensaje = f'¡Hecho! La {titulo} se ha modificado exitosamente.'
    comision = Comision.objects.get(id=pk)
    if request.method == 'POST':
        form = ComisionUptadeForm(request.POST, instance=comision)
        if form.is_valid():
            form.save()
            messages.info(request, mensaje)
            return redirect('comisiones')
    else:
        form = ComisionUptadeForm(instance=comision)
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "comision/modificar.html", context)
