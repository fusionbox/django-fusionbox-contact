from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from fusionbox.mail import send_markdown_mail

from fusionbox.contact.forms import ContactForm
from fusionbox.contact.models import Recipient


class SubmissionCreate(CreateView):
    """
    class-based-view for handling contact form submissions.  By default, this
    uses the template found at ``contact/index.html``.
    """
    email_template = 'mail/contact_form_submission.html'
    template_name = 'contact/index.html'

    def get_form_class(self):
        """
        Returns :class:`fusionbox.contact.forms.ContactForm`
        """
        return ContactForm

    def form_valid(self, form):
        """
        Saves the new contact form submission and sends successful submission
        email.
        """
        try:
            recipients = settings.CONTACT_FORM_RECIPIENTS
        except AttributeError:
            recipients = Recipient.objects.filter(is_active=True).values_list('email', flat=True)
        env = {'submission': form.save()}
        if recipients:
            send_markdown_mail(self.email_template, env, to=recipients)
        return super(SubmissionCreate, self).form_valid(form)

    def get_success_url(self):
        """
        Returns whatever url has been registered under the name
        `contact_success`.
        """
        return reverse('contact_success')

index = SubmissionCreate.as_view()


class SubmissionSuccess(TemplateView):
    """
    class-based-view for rendering the contact form success page.
    """
    template_name = 'contact/success.html'

success = SubmissionSuccess.as_view()
