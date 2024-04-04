from codicefiscale import codicefiscale
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from clinux import settings


class Gender(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    OTHER = "O", _("Other")


def check_italian_social_id(code: str):
    """Check if an italian social id is formally valid"""
    if not codicefiscale.is_valid(code):
        raise ValidationError(_(f"Social ID {code} is formally invalid"))


class Member(models.Model):
    """A member of the association"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("User"),
        related_name="member",
    )

    social_id = models.CharField(
        _("Social ID"),
        max_length=16,
        validators=[check_italian_social_id],
    )

    gender = models.CharField(_("Gender"), max_length=1, choices=Gender.choices)

    birth_date = models.DateField(_("Birth Date"))
    birth_city = models.CharField(
        _("Birth City"),
        max_length=150,
        help_text=_("City/municipality or foreign country where Member is born"),
    )
    # TODO: Province/Region require a separate structure
    # birth_province = models.ForeignKey(
    #     Region,
    #     on_delete=models.PROTECT,
    #     verbose_name=_("Birth Province"),
    #     help_text=_("Birth Region (EE for other countries)"),
    # )
    # birth_country = models.CharField(_("Birth Country"), max_length=...)

    phone = models.CharField(
        _("Phone Number"),
        max_length=50,
        help_text=_("Phone Number, use only digits, +, -, space and parenthesis"),
        validators=[
            RegexValidator(
                r"^(00|\+)?((\d+|\(\d+\))[ \-]?)+\d$",
                _("Use only plus sign (at start), dashes (-), spaces and parenthesis"),
            )
        ],
    )

    def get_absolute_url(self):
        return reverse("member", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.social_id})"

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
