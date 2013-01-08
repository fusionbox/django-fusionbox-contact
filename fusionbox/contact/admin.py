from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fusionbox.contact.models import Submission, Recipient
from fusionbox.admin import CsvAdmin


class SubmissionAdmin(admin.ModelAdmin, CsvAdmin):
    """
    Default admin class for ``fusionbox.contact.models.Submission``.  Allows
    for bulk csv export of ``Submission`` entries, and restricts readonly
    access.
    """
    list_display = ('name', 'email', 'list_comment', 'created_at')
    date_hierarchy = 'created_at'

    class Media:
        """
        Ensures that whitespace linebreaks are respected when displaying the
        ``Submission.comment`` field.
        """
        css = {
                'all': ('contact.css',)
                }

    def get_readonly_fields(self, request, obj=None):
        """
        Dynamically build a list of field names for the model.  This allows for
        monkeypatches to the ``Submission`` model to not require a new admin
        class.
        """
        return [field.attname for field in self.model._meta.fields if not field.primary_key]

    def list_comment(self, submission):
        """
        Allows for display of a truncated version of ``Submission.comment`` in
        the list_display.
        """
        return submission.comment[:200]
    list_comment.short_description = _('Comment')

    def has_add_permission(self, *args, **kwargs):
        """
        Submissions should not be creatable from the admin center.
        """
        return False


class RecipientAdmin(admin.ModelAdmin):
    """
    Defauld admin class for ``fusionbox.contact.models.Recipient``.  Only
    registered if no hard-coded list of recipients is found in
    ``settings.CONTACT_FORM_RECIPIENTS``.
    """
    list_display = ('name', 'email', 'is_active')
    fieldsets = (
                (None, {
                    'fields': ('name', 'email', 'is_active'),
                    'description': _(u'Use this form to add or change a recipient for contact form submissions.'),
                    }),
            )

admin.site.register(Submission, SubmissionAdmin)

# Only register the Recipient model if no hard-coded list of recipients was found
if hasattr(settings, 'CONTACT_FORM_RECIPIENTS'):
    pass
else:
    admin.site.register(Recipient, RecipientAdmin)
