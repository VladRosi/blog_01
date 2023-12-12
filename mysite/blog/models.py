from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset()\
                  .filter(status=Post.Status.PUBLISHED)


class DraftManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset()\
                  .filter(status=Post.Status.DRAFT)


class Post(models.Model):
  class Status(models.TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'PB', 'Published'

  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
  body = models.TextField()
  publish = models.DateTimeField(default=timezone.now)
  created = models.DateTimeField(auto_now_add=True)
  update = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

  objects = models.Manager()
  published = PublishedManager()
  draft = DraftManager()

  class Meta:
    default_manager_name = 'objects'
    ordering = ['-publish']
    indexes = [
      models.Index(fields=['-publish']),
    ]

  def __str__(self):
    return self.title
