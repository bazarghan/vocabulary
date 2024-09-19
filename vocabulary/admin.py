from django.contrib import admin
from .models import Vocabulary, Definition, Source

admin.site.register(Vocabulary)
admin.site.register(Definition)
admin.site.register(Source)
