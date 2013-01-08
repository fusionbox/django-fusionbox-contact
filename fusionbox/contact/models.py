from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _, ugettext_noop

from fusionbox import behaviors

SUBMISSION_VERBOSE_NAME = getattr(settings, 'CONTACT_SUBMISSION_VERBOSE_NAME', None)
SUBMISSION_VERBOSE_NAME_PLURAL = getattr(settings, 'CONTACT_SUBMISSION_VERBOSE_NAME_PLURAL', None)

RECIPIENT_VERBOSE_NAME = getattr(settings, 'CONTACT_RECIPIENT_VERBOSE_NAME', None)
RECIPIENT_VERBOSE_NAME_PLURAL = getattr(settings, 'CONTACT_RECIPIENT_VERBOSE_NAME_PLURAL', None)

ugettext_noop('Contact')


class Submission(behaviors.Timestampable):
    name = models.CharField(verbose_name=_('name'), max_length=200)
    email = models.EmailField(verbose_name=_('email'), max_length=320)
    comment = models.TextField(verbose_name=_('comment'), blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = SUBMISSION_VERBOSE_NAME or _('submission')
        verbose_name_plural = SUBMISSION_VERBOSE_NAME_PLURAL or _('submissions')

    def get_absolute_url(self):
        return reverse('admin:{0}_{1}_change'.format(
            self._meta.app_label,
            self._meta.module_name,
            ), args=(self.id,))


class Recipient(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=200)
    email = models.EmailField(verbose_name=_('email'), max_length=320)
    is_active = models.BooleanField(verbose_name=_('is active'),
                                    help_text=_(u"Only recipients with this"
                                                " field checked will receive"
                                                " contact form submissions."))

    class Meta:
        ordering = ('name', 'email')
        verbose_name = RECIPIENT_VERBOSE_NAME or _('recipient')
        verbose_name_plural = RECIPIENT_VERBOSE_NAME_PLURAL or _('recipients')
