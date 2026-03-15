from pathlib import Path
import csv
from django.core.management.base import BaseCommand
from core.models import MelanomaMortalityStatistic


class Command(BaseCommand):
    help = "Import melanoma mortality data"

    def handle(self, *args, **kwargs):
        csv_path = Path("../data/mortality_melanoma.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        MelanomaMortalityStatistic.objects.all().delete()

        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            self.stdout.write(f"Detected columns: {reader.fieldnames}")

            for row in reader:
                normalized_row = {k.strip(): v for k, v in row.items() if k}

                year = int(normalized_row["Year"])
                sex = normalized_row["Sex"].strip()
                age_group = normalized_row["Age group (years)"].strip()

                rate_str = (normalized_row.get("Age-specific rate(per 100,000)") or "").strip()

                mortality_rate = float(rate_str) if rate_str else 0.0

                MelanomaMortalityStatistic.objects.create(
                    year=year,
                    mortality_rate=mortality_rate,
                    age_group=age_group,
                    sex=sex,
                )

        self.stdout.write(self.style.SUCCESS("Mortality import completed"))
        self.stdout.write(f"Total records: {MelanomaMortalityStatistic.objects.count()}")