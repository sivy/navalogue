import markdown
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe, strip_tags
from tenants.models import Tenant

app_name = "weblog"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name


# Create your models here.
class Entry(models.Model):
    created = models.DateTimeField(default=timezone.now)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    slug = models.SlugField(max_length=512)
    meta = models.JSONField(default=dict, blank=True)
    posttype = models.CharField(
        max_length=12,
        default="post",
        choices=[
            ("post", "Post"),
            ("note", "Note"),
        ],
    )
    summary = models.TextField(default="", blank=True)
    body = models.TextField()

    authors = models.ManyToManyField(User, through="Authorship")
    tags = models.ManyToManyField(Tag, blank=True)

    image = models.ImageField(upload_to="static/uploads/", null=True, blank=True)
    card_image = models.URLField(
        blank=True, null=True, help_text="URL to image for social media cards"
    )

    is_draft = models.BooleanField(
        default=False,
        help_text="Draft entries do not show in index pages but can be visited directly if you know the URL",
    )

    class Meta:
        verbose_name_plural = "entries"

    @property
    def title_or_snippet(self):
        return self.title or f"{self.body[:50]} (no title)"

    @property
    def summary_rendered(self):
        return mark_safe(markdown.markdown(self.summary, output_format="html5"))

    @property
    def summary_text(self):
        if self.summary:
            return strip_tags(markdown.markdown(self.summary, output_format="html5"))
        else:
            return strip_tags(markdown.markdown(self.body, output_format="html5"))[:300]

    @property
    def body_rendered(self):
        return mark_safe(markdown.markdown(self.body, output_format="html5"))

    def get_absolute_url(self):
        return "/%d/%d/%d/%s" % (
            self.created.year,
            self.created.month,
            self.created.day,
            self.slug,
        )

    def __str__(self):
        return self.title


class Authorship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
