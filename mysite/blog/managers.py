from django.db import models as db_modules
from blog import models as blog_models


class PublishedManager(db_modules.Manager):
  def get_queryset(self):
    return super().get_queryset()\
                  .filter(status=blog_models.Post.Status.PUBLISHED)


class DraftManager(db_modules.Manager):
  def get_queryset(self):
    return super().get_queryset()\
                  .filter(status=blog_models.Post.Status.DRAFT)
