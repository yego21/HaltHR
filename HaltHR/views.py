from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView

from company.admin import Event_ScheduleInline
from company.models import Event, Announcement, Event_Schedule
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import OuterRef, Subquery
from django.utils import timezone


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

        # Subquery to get the first schedule's date
        first_schedule = Event_Schedule.objects.filter(event=OuterRef('pk')).order_by('date')

        # Annotate with the earliest date from event_schedule
        event_list = Event.objects.filter(event_schedule__isnull=False).annotate(
            first_schedule_date=Subquery(first_schedule.values('date')[:1])
        ).distinct().order_by('-first_schedule_date')

        # Separate into past and upcoming events
        past_event_list = event_list.filter(first_schedule_date__lt=timezone.now()).order_by('-first_schedule_date')
        upcoming_event_list = event_list.filter(first_schedule_date__gte=timezone.now()).order_by('first_schedule_date')

        # Set up pagination
        paginator = Paginator(event_list, 12)  # Show 6 events per page

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)  # If page is not an integer, deliver the first page.
        except EmptyPage:
            events = paginator.page(paginator.num_pages)  # If page is out of range, deliver the last page of results.

        context['events'] = events
        context['past_events'] = past_event_list
        context['upcoming_events'] = upcoming_event_list




        return context
