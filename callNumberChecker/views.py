# from django import forms
from django.views.generic.edit import FormView
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from django import forms
from django.shortcuts import redirect

from .forms import ContactForm
from .models import RecordID

class IndexView(FormView):
    form_class = ContactForm
    template_name = 'callNumberChecker/index.html'
    success_url = reverse_lazy('callNumberChecker:index')
    model = RecordID

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        recordid = RecordID.objects.all()
        kwargs['recordid'] = recordid
        kwargs['len_of_recordid'] = len(recordid)
        if len(recordid):
            kwargs['last_callNumber_is_right'] = recordid[len(recordid)-1].is_right_callNumber == True
            kwargs['last_callNumber_is_wrong'] = recordid[len(recordid)-1].is_right_callNumber == False
        else: kwargs['last_callNumber_is_right'] = kwargs['last_callNumber_is_wrong'] = False

        kwargs['right_count'] = len(list(filter(
            lambda x: x.is_right_callNumber == True, recordid)))
        kwargs['wrong_count'] = len(list(filter(
            lambda x: x.is_right_callNumber == False, recordid)))
        context = super().get_context_data(**kwargs)
        return context

class OutputView(generic.DetailView):

    def dispatch(self, *args, **kwargs):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=record_id.txt'
        # Designate The Model
        recordid = RecordID.objects.filter(is_right_callNumber = True)

        # Create blank list
        lines = []
        # Loop Thu and output
        for id in recordid:
            lines.append('{}\n'.format(id.record_id))
        response.writelines(lines)
        return response

class ResetView(generic.DetailView):

    def dispatch(self, *args, **kwargs):
        RecordID.objects.all().delete()
        response = redirect('callNumberChecker:index')
        return response