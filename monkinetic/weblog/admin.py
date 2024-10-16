from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Entry, Tag


class AuthorsInlineAdmin(admin.TabularInline):
    model = Entry.authors.through


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = [
        "title_or_snippet",
        "slug",
        "created",
    ]
    fields = [
        "created",
        "slug",
        "body",
        "summary",
        "image",
        "card_image",
        "tags",
        "meta",
    ]
    empty_value_display = ""
    ordering = ["-created"]
    inlines = (AuthorsInlineAdmin,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]
