from django.contrib import admin

# Register your models here.
from . import models
# Register your models here.
register_list = [
    models.Flavor,
    models.BackingFile,
    models.VMTemplate,
]

admin.site.register(register_list)