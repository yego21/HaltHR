import csv
import pandas as pd
from django.http import HttpResponse
from clocker.models import Clocker
import pytz

def export_clocker_to_csv(queryset, user):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clocker_entries.csv"'

    writer = csv.writer(response)
    writer.writerow([f'Clocker entries for {user.full_name}'])
    writer.writerow(['Date', 'In Time', 'Out Time', 'Remarks'])

    for clocker in queryset:
        writer.writerow([clocker.date, clocker.time_in, clocker.time_out, clocker.calculate_time_difference])

    return response


def export_clocker_to_xls(queryset, user):
    # Convert datetime fields to strings
    # Define your local timezone
    local_tz = pytz.timezone('Asia/Manila')  # Replace with your desired timezone

    # Convert the queryset to a list of dictionaries and handle datetime conversion
    data = []
    for clocker in queryset:
        date_str = clocker.date.strftime('%Y-%m-%d')
        time_in_str = clocker.time_in.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S') if clocker.time_in else ''
        time_out_str = clocker.time_out.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S') if clocker.time_out else ''
        remarks = clocker.calculate_time_difference

        data.append({
            'Date': date_str,
            'In Time': time_in_str,
            'Out Time': time_out_str,
            'Remarks': remarks,
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="clocker_entries_{user.full_name}.xlsx"'
    df.to_excel(response, index=False, sheet_name='Clocker Entries')
    return response
