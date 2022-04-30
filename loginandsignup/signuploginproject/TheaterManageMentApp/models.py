from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class AdminRegisterModel(models.Model):
    AdminId = models.CharField(max_length=250)
    Email = models.EmailField(max_length=50)

    Password = models.CharField(max_length=50)

    MobileNumber = models.CharField(max_length=13, unique=True)
    CreatedDate = models.CharField(max_length=250)
    UpdatedDate = models.CharField(max_length=250)
    Status = models.CharField(max_length=250)
    objects = models.Manager

    class Meta:
        db_table = "AdminRegisterTable"


class OtpModel(models.Model):
    HcpId = models.ForeignKey(AdminRegisterModel, on_delete=models.CASCADE, related_name='otp', default=True)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    objects = models.Manager

    class Meta:
        db_table = "OtpTable"


class MovieListModel(models.Model):
    class Status(models.TextChoices):
        Open = 'Open'
        Closed = 'Closed'

    MovieId = models.CharField(max_length=250)
    ReleaseDate = models.TimeField()
    CloseDate = models.TimeField()
    Rating = models.IntegerField()
    CreatedTime = models.TimeField()
    UpdatedTime = models.TimeField()
    Status = models.CharField(max_length=10, choices=Status.choices)
    objects = models.Manager

    class Meta:
        db_table = "MoviesTable"

