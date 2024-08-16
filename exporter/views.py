from django.shortcuts import render
from .exports import export_clocker_to_csv, export_clocker_to_xls
from clocker.models import Clocker


def export_clocker_entries(request):
    user_id = request.GET.get('user_id')
    queryset = Clocker.objects.filter(user_id=user_id)

    if request.GET.get('format') == 'csv':
        return export_clocker_to_csv(queryset)
    elif request.GET.get('format') == 'excel':
        return export_clocker_to_xls(queryset)
    return render(request, 'clocker/clocker_popup.html', {'queryset': queryset})
