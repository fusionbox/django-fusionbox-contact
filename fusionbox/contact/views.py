from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from fusionbox.mail import send_markdown_mail

from fusionbox.contact.forms import ContactForm
from fusionbox.contact.models import Recipient


class SubmissionCreate(CreateView):
    email_template = 'mail/contact_form_submission.html'
    template_name = 'contact/index.html'

    def get_form_class(self):
        return ContactForm

    def form_valid(self, form):
        try:
            recipients = settings.CONTACT_FORM_RECIPIENTS
        except AttributeError:
            recipients = Recipient.objects.filter(is_active=True).values_list('email', flat=True)
        env = {'submission': form.instance}
        if recipients:
            send_markdown_mail(self.email_template, env, to=recipients)
        return super(SubmissionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('contact_success')

index = SubmissionCreate.as_view()


class SubmissionSuccess(TemplateView):
    template_name = 'contact/success.html'

    def get_context_data(self, **kwargs):
        context = super(SubmissionSuccess, self).get_context_data(**kwargs)
        context['site_name'] = getattr(settings, 'SITE_NAME', 'us')
        return context

success = SubmissionSuccess.as_view()
