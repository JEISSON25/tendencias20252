import django_filters
from .models import pickingModel

class PickingFilter(django_filters.FilterSet):
    # ✅ Filtro para Fecha de Inicio (mayor o igual: __gte)
    date_start= django_filters.DateFilter(
        field_name='fecha_procesamiento',
        lookup_expr='gte'
    )
    
    # ✅ Filtro para Fecha Final (menor o igual: __lte)
    date_end=django_filters.DateFilter(
        field_name='fecha_procesamiento',
        lookup_expr='lte'
    )
    
    origen = django_filters.CharFilter(
        field_name='origen',
        lookup_expr='exact'
    )
    
    class Meta:
        model = pickingModel
        fields = ['fecha_procesamiento', 'origen']
        
        