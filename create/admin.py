from django.contrib import admin

# Register your models here.
from . import models
# Register your models here.
register_list = [
    models.Flavor,
    models.BackingFile,
    models.VMTemplate,
    models.QuickVM,
    models.QuickVMStep,
]

admin.site.register(register_list)