import datetime
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'
    login_url =  reverse_lazy('users_app:login')


class DateMixin(object):

    def get_context_data(self, **kwargs):
        context = super(DateMixin, self).get_context_data(**kwargs)
        context['date'] = datetime.datetime.now()
        return context


class TemplatePruebaMixin(DateMixin, TemplateView):
    template_name = 'home/mixin.html'