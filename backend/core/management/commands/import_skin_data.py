import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from core.models import CancerStatistic


class Command(BaseCommand):
    help = "Import melanoma data"

    def handle(self, *args, **kwargs):
        csv_path = Path("../data/skin_melanoma.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        CancerStatistic.objects.all().delete()

        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                CancerStatistic.objects.create(
                    year=int(row["Year"]),
                    incidence_rate=float(row["Age-specific rate(per 100,000)"]),
                    age_group=row["Age group (years)"],
                    sex=row["Sex"]
                )

        self.stdout.write(self.style.SUCCESS("Import completed"))
        self.stdout.write(f"Total records: {CancerStatistic.objects.count()}")