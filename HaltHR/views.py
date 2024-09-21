from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from company.models import Event, Announcement
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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

        # Get the page number from the request
        page = self.request.GET.get('page')

        # Fetch announcements and events
        context['announcements'] = Announcement.objects.order_by('-date_posted')
        event_list = Event.objects.order_by('-date')

        # Set up pagination
        paginator = Paginator(event_list, 6)  # Show 6 events per page

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)  # If page is not an integer, deliver the first page.
        except EmptyPage:
            events = paginator.page(paginator.num_pages)  # If page is out of range, deliver the last page of results.

        context['events'] = events

        return context
