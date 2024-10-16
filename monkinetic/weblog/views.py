# Create your views here.
from django.contrib.syndication.views import Feed
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.utils.feedgenerator import Atom1Feed

from .forms import PostForm, EntryForm
from .models import Entry, Tag

ENTRIES_ON_HOMEPAGE = 20


def index(request):
    entries = list(
        Entry.objects.prefetch_related("tags")
        .filter(
            tenant=request.tenant,
            is_draft=False,
        )
        .order_by("-created")[: ENTRIES_ON_HOMEPAGE + 1]
    )
    has_more = False
    if len(entries) > ENTRIES_ON_HOMEPAGE:
        has_more = True
        entries = entries[:ENTRIES_ON_HOMEPAGE]

    return render(
        request,
        f"weblog/{request.tenant}/index.jinja",
        {"entries": entries, "has_more": has_more, "form": PostForm()},
    )


def view_entry(request, year, month, day, slug):
    entry = get_object_or_404(Entry, slug=slug)
    return render(request, f"weblog/{request.tenant}/entry.jinja", {"entry": entry})


def add_entry(request):
    form = PostForm(request.POST)
    if form.is_valid():
        _body = form.cleaned_data["body"]
        _type = "note"
        _tags = form.cleaned_data["tags"]

        e = Entry(tenant=request.tenant, body=_body, posttype=_type)
        e.save()

        e.slug = f"note-{e.id}"
        e.authors.add(request.user)

        for tag in _tags:
            tag = Tag.objects.get(tag)
            e.tags.add(tag)
        e.save()
    else:
        form = EntryForm(request.POST)
        entry = form.save()
        entry.user = request.user
    return HttpResponseRedirect(reverse("weblog:index"))


class BlogFeed(Feed):
    title = "Navalogue"
    link = "/"
    feed_type = Atom1Feed

    def items(self):
        return Entry.objects.filter(is_draft=False).order_by("-created")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary_rendered + "\n" + item.body_rendered

    def item_link(self, item):
        return "/blog/%d/%s/" % (item.created.year, item.slug)

    def item_author_name(self, item):
        return ", ".join([a.get_full_name() or str(a) for a in item.authors.all()]) or None

    def get_feed(self, obj, request):
        feedgen = super().get_feed(obj, request)
        feedgen.content_type = "application/xml; charset=utf-8"
        return feedgen
