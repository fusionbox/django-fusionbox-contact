from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from fusionbox import behaviors

SUBMISSION_VERBOSE_NAME = getattr(settings, 'CONTACT_SUBMISSION_VERBOSE_NAME', None)
SUBMISSION_VERBOSE_NAME_PLURAL = getattr(settings, 'CONTACT_SUBMISSION_VERBOSE_NAME_PLURAL', None)

RECIPIENT_VERBOSE_NAME = getattr(settings, 'CONTACT_RECIPIENT_VERBOSE_NAME', None)
RECIPIENT_VERBOSE_NAME_PLURAL = getattr(settings, 'CONTACT_RECIPIENT_VERBOSE_NAME_PLURAL', None)


class Submission(behaviors.Timestampable):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=320)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = SUBMISSION_VERBOSE_NAME
        verbose_name_plural = SUBMISSION_VERBOSE_NAME_PLURAL

    def get_absolute_url(self):
        return reverse('admin:{0}_{1}_change'.format(
            self._meta.app_label,
            self._meta.module_name,
            ), args=(self.id,))


class Recipient(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=320)
    is_active = models.BooleanField(help_text=u"Only recipients with this field checked will receive contact form submissions")

    class Meta:
        ordering = ('name', 'email')
        verbose_name = RECIPIENT_VERBOSE_NAME
        verbose_name_plural = RECIPIENT_VERBOSE_NAME_PLURAL
