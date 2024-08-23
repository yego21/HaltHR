from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from company.models import Event, Announcement
from django.utils.decorators import method_decorator


# @login_required
# def index(request):
#     # def event_viewer(data):
#     #     events = Event.objects.order_by('-date')
#     #     print(events)
#     #     data = 'yeayea'
#     #     return data
#     def get_events():
#         events = Event.objects.order_by('-date')
#         return events
#     data ='yeayea'
#     events = get_events()
#
#         # return render(request, 'index.html', {'events': events, 'data': data})
#
#
#     return render(request, 'index.html', {'data': data, 'events': events})



@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['announcements'] = Announcement.objects.order_by('-date_posted')
        context['events'] = Event.objects.order_by('-date')
        return context