
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProjectData(models.Model):
    fk_user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    int_opend_issues = models.IntegerField(blank=True, null=True)
    int_commits = models.IntegerField(blank=True, null=True)
    int_doing_issues = models.IntegerField(blank=True, null=True)
    dat_fetching = models.DateTimeField()

    def __str__(self):
        return "{}".format(self.id)
