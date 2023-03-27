from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from events.compat import login_required
from events.models import EventType, EVENT_MEDIA, send
from events.utils import event_filter_for_user, create_filter_for_user


class EventFilterView(TemplateView):
    template_name = "events/events_filters.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventFilterView, self).dispatch(*args, **kwargs)

    @property
    def scoping(self):
        return None

    def filter_for_user(self, event_type, action_id):
        return event_filter_for_user(
            self.request.user,
            event_type,
            action_id,
            scoping=self.scoping
        )

    def form_label(self, event_type, action_id):
        return "setting-{0}-{1}".format(
            event_type.pk,
            action_id
        )

    def process_cell(self, label):
        '''
        @todo: change according to our model. if val is on then delete corresponding entry else create it
        '''
        val = self.request.POST.get(label)
        print("process_cell: ", label, "val ", val)
        _, pk, action_id = label.split("-")
        event_type = EventType.objects.get(pk=pk)
        setting = self.filter_for_user(event_type, action_id)
        if val == "on" and setting:
            setting.delete()
        elif setting is None and val is None:
            create_filter_for_user(self.request.user, event_type, action_id)
        else:
            print("process_cell: Nothing to do for ", label)

    def settings_table(self):
        event_types = EventType.objects.all()
        table = []
        for event_type in event_types:
            row = []
            for action_id, medium_display in EVENT_MEDIA:
                setting = self.filter_for_user(event_type, action_id)
                val = bool(setting is None)
                row.append((
                    self.form_label(event_type, action_id),
                    val)
                )
            table.append({"event_type": event_type, "cells": row})
        return table

    def post(self, request, *args, **kwargs):
        table = self.settings_table()
        for row in table:
            for cell in row["cells"]:
                self.process_cell(cell[0])
        return HttpResponseRedirect(request.POST.get("next_page", "."))

    def get_context_data(self, **kwargs):
        filters = {
            "column_headers": [
                medium_display
                for _, medium_display in EVENT_MEDIA
            ],
            "rows": self.settings_table(),
        }
        context = super(EventFilterView, self).get_context_data(**kwargs)
        context.update({
            "event_types": EventType.objects.all(),
            "event_filters": filters
        })
        return context

    
    