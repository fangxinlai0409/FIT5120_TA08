from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(TimeStampedModel):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="Melbourne")
    state = models.CharField(max_length=100, default="Victoria")
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"


class UVReading(TimeStampedModel):
    location = models.ForeignKey(Location, related_name="uv_readings", on_delete=models.CASCADE)
    uv_index = models.DecimalField(max_digits=4, decimal_places=1)
    risk_level = models.CharField(max_length=20)
    observation_time = models.DateTimeField()
    burn_time_minutes = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-observation_time"]


class CancerStatistic(TimeStampedModel):
    year = models.PositiveIntegerField()
    incidence_rate = models.DecimalField(max_digits=6, decimal_places=2, help_text="Cases per 100k")
    age_group = models.CharField(max_length=50, default="All ages")

    class Meta:
        ordering = ["year"]


class ProtectionRule(TimeStampedModel):
    min_uv = models.DecimalField(max_digits=4, decimal_places=1)
    max_uv = models.DecimalField(max_digits=4, decimal_places=1)
    label = models.CharField(max_length=50)
    recommendation = models.TextField()

    class Meta:
        ordering = ["min_uv"]

    def matches(self, uv_value: float) -> bool:
        return float(self.min_uv) <= uv_value <= float(self.max_uv)
