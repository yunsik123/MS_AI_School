from django.db import models

from ai.models import BaseModel


class OpenaiMessage(BaseModel):

    class Meta:
        verbose_name = verbose_name_plural = "OpenAI 메시지"

    def __str__(self):
        return self.message

    message = models.TextField(null=True, blank=True, verbose_name="메시지")
