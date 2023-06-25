from django.contrib import admin
from .models.dog_models import DogZukan
from .models.cat_models import CatZukan


class DogZukanAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_public']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_public',]


class CatZukanAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_public']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_public',]


admin.site.register(DogZukan, DogZukanAdmin)
admin.site.register(CatZukan, CatZukanAdmin)