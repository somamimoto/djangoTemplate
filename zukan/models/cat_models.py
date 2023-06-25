from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class CatZukan(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.CharField(max_length=40, unique=True)
    image = models.ImageField(upload_to='zukan/cat/')
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('zukan:detail', kwargs={'category_slug': 'cat', 'slug': self.slug})
