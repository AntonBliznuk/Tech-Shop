from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.ImageProduct)
admin.site.register(models.ViewProduct)
admin.site.register(models.WhisList)
