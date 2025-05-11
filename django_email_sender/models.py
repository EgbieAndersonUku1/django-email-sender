from django.db import models
from django.utils.translation import gettext_lazy as _


class EmailBaseLog(models.Model):
    """The base email class"""
    
    from_email     = models.EmailField(db_index=True, max_length=100)
    to_email       = models.EmailField(db_index=True, max_length=200)
    subject        = models.CharField(max_length=100)
    sent_on        = models.DateTimeField(auto_now_add=True)
    email_body     = models.TextField()
    status         = models.CharField(max_length=50)
    created_on     = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return _("{} -> {} with subject {}").format(
            self.from_email,
            self.to_email,
            self.subject
        )

