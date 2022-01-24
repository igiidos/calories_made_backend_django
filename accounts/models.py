import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):  # 1:1
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    sex = models.PositiveSmallIntegerField(blank=True, null=True)  # 1이면 남자, 2이면 여자 3이면 중성
    birth = models.DateField(null=True, blank=True)  # 생일
    height = models.PositiveIntegerField(blank=True, null=True)  # 키 cm
    weight = models.PositiveIntegerField(blank=True, null=True)  # 몸무게 kg

    def __str__(self):
        return self.user.username


class Token(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='account_auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return f"{self.key} | {self.user.username}"
