from django.db import models
from django.core.urlresolvers import reverse

from fusionbox import behaviors


class Submission(behaviors.Timestampable):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=320)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ('-created_at',)

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
