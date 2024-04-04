from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Member


class MemberDetailView(DetailView):
    model = Member
    context_object_name = "member"
    template_name = "members/member.html"


class MemberListView(ListView):
    model = Member
    context_object_name = "members"

'''
class RegistrationForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField(widget=forms.Textarea)
    

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
'''

class RegistrationView(LoginRequiredMixin,CreateView):
    login_url = "/auth/login/"
    model = Member
    template_name = "members/registration.html"
    fields = [field.name for field in Member._meta.fields if "user" not in field.name]
    success_url = reverse_lazy("home")  

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)