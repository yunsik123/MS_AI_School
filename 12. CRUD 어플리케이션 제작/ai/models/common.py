import datetime
import uuid
from django.db import models


class BaseQuerySet(models.query.QuerySet):
    def delete(self):
        self.update(removed_at=datetime.datetime.now())
        # super(BaseQuerySet, self).delete()


class ModelManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model).filter(removed_at=None)
        # return super(ModelManager, self).get_queryset().filter(removed_at=None)


class BaseModel(models.Model):
    objects = ModelManager()

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="생성일")
    removed_at = models.DateTimeField(null=True, blank=True, verbose_name='삭제일')
