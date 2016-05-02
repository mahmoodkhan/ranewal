import os

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .models import ItemAttachment


# Delete file when ItemAttachment object is deleted from the db.
@receiver(models.signals.post_delete, sender=ItemAttachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding 'ItemAttachment' is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


