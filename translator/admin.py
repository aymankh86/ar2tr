from django.contrib import admin
from .models import Category, Phrase, Suggestions

admin.site.register(Category)
admin.site.register(Phrase)
admin.site.register(Suggestions)
