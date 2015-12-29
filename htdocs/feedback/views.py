from django.shortcuts import render

from django.views.generic import TemplateView, FormView, View, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.utils import timezone

from django.contrib.messages.views import SuccessMessageMixin

from .models import Feedback
from .forms import *
#from .mixins import AjaxFormResponseMixin, LoginRequiredMixin, PurchaseRequestMixin
#from .serializers import FlatJsonSerializer

class FeedbackListView(ListView):
    """
    PR List View
    """
    model = Feedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedback'


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'epro/feedback.html'
    success_message = "Your request: %(summary)s is sent."

    def form_valid(self, form):
        form.instance.created_by = self.request.user.userprofile
        return super(FeedbackCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, summary=self.object.summary)

