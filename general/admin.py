from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Intern)
admin.site.register(Organization)
admin.site.register(HashTags)
admin.site.register(Comment)