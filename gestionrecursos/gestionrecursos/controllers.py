from apps.recursos.models import Recursos
from apps.reservas.models import Reservas
from apps.usuarios.models import Usuarios
from apps.roles.models import Roles
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

# Vista inicial
def initial_view(request):
    if request.user.is_authenticated:
        if request.user.rol:
            if request.user.rol.id_rol == 1:
                return redirect('home')
            return redirect('home')
        return redirect('home')

    return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')

# Vista de login con template
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = Usuarios.objects.filter(username=username).first()
        if not user:
            return render(request, 'login.html', {'error': 'Usuario no encontrado'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.rol:
                if request.user.rol.id_rol == 1:
                    return redirect('home')
                return redirect('home')
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')


# Vista principal protegida
@login_required(login_url='/login/')
def home_view(request):
    module = request.GET.get('module', 'dashboard')
    roles = Roles.objects.all()
    users = Usuarios.objects.all()
    tipo_recurso = [v for v, _ in Recursos._meta.get_field('estado_recurso').choices]

    return render(request, 'home.html', {
        'module': module,
        'roles': roles,
        'users': users,
        'tipo_recurso': tipo_recurso
    })

@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login/')
def dashboard_metrics(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("No autenticado")

    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)

    # 1) Cantidad de recursos disponibles y reservas activas
    recursos_disponibles = Recursos.objects.filter(estado_recurso='DISPONIBLE').count()

    reservas_activas_qs = Reservas.objects.filter(
        estado_reserva__in=["PENDIENTE", "CONFIRMADA"],
        fecha_fin__gt=now
    )
    reservas_activas = reservas_activas_qs.count()

    # 2) Cantidad de usuarios
    usuarios_registrados = Usuarios.objects.count()

    # 3) Top de recursos más reservados (top 5)
    top_recursos = (
        Reservas.objects.values('id_recurso__id_recurso', 'id_recurso__nombre_recurso')
        .annotate(total=Count('id_reserva'))
        .order_by('-total')[:5]
    )
    top_labels = [item['id_recurso__nombre_recurso'] or item['id_recurso__id_recurso'] for item in top_recursos]
    top_values = [item['total'] for item in top_recursos]

    data = {
        'recursos': {
            'disponibles': recursos_disponibles,
            'reservas_activas': reservas_activas,
        },
        'usuarios': {
            'registrados': usuarios_registrados,
        },
        'top_recursos': {
            'labels': top_labels,
            'values': top_values,
        },
        'generado_en': now.isoformat(),
    }

    return JsonResponse(data)
