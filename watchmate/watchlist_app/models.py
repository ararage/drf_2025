import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class AbstractAuditModel(models.Model):
    """
    BaseModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        "created_at",
        auto_now_add=True,
        help_text="Date time on which the object was created.",
    )
    modified = models.DateTimeField(
        "modified_at",
        auto_now=True,
        help_text="Date time on which the object was last modified.",
    )
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class AbstractUUIDAuditModel(AbstractAuditModel):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )

    class Meta:
        abstract = True


class StreamPlatform(AbstractUUIDAuditModel):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=500)

    def __str__(self):
        return self.name


class WatchList(AbstractUUIDAuditModel):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    platform = models.ForeignKey(
        StreamPlatform,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="watchlist",
    )

    def __str__(self):
        return self.title


class Reviews(AbstractUUIDAuditModel):
    review_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
        default=None,
    )
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(
        WatchList,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )

    def __str__(self):
        return (
            str(self.rating) + " ⭐ " + self.watchlist.title if self.watchlist else ""
        )
