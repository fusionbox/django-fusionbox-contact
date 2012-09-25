from fusionbox.forms.models import UncaptchaModelForm

from fusionbox.contact.models import Submission


class ContactForm(UncaptchaModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Submission
        exclude = ('created_at',)
