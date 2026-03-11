from django.core.management.base import BaseCommand

from core.models import CancerStatistic, ProtectionRule

CANCER_STATS = [
    (2013, 49.8),
    (2014, 50.5),
    (2015, 51.2),
    (2016, 52.1),
    (2017, 53.0),
    (2018, 54.4),
    (2019, 55.3),
    (2020, 56.1),
    (2021, 56.8),
]

PROTECTION_RULES = [
    (0, 2, "Low", "Minimal protection required. Keep sunscreen handy."),
    (3, 5, "Moderate", "Apply SPF50+, wear sunglasses and consider a hat."),
    (6, 7, "High", "Wear SPF50+, sunglasses, and long-sleeve shirts."),
    (8, 10, "Very High", "Add shade breaks, broad-brim hat, and reapply sunscreen."),
    (11, 15, "Extreme", "Avoid direct sun, cover up fully, seek shade immediately."),
]


class Command(BaseCommand):
    help = "Seeds baseline CancerStatistic and ProtectionRule records."

    def handle(self, *args, **options):
        for year, rate in CANCER_STATS:
            CancerStatistic.objects.update_or_create(
                year=year,
                defaults={"incidence_rate": rate, "age_group": "All ages"},
            )

        for min_uv, max_uv, label, text in PROTECTION_RULES:
            ProtectionRule.objects.update_or_create(
                label=label,
                defaults={
                    "min_uv": min_uv,
                    "max_uv": max_uv,
                    "recommendation": text,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed data created or refreshed."))
