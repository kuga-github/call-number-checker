from django.db import models

class RecordID(models.Model):
  record_id = models.CharField(max_length=13, default='0000000', editable=False)
  cTop = models.CharField(max_length=10, default='0000000', editable=False)
  cMdl = models.CharField(max_length=10, default='0000000', editable=False)
  cBtm = models.CharField(max_length=10, default='0000000', editable=False)
  is_right_callNumber = models.BooleanField(default=True)

  def __str__(self):
        return self.record_id