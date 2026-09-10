"""
One-off data fix: link each Butterfly record's Butterfly_Map_Image field
to the matching file already sitting in media/Images/Butterfly_Maps/.

Those files were never linked to the DB (the CSV import only sets text/number
fields, not file fields, and nobody has uploaded a map via /admin yet), so the
field is blank for every butterfly even though the images already exist on disk.

Usage (from the eon/ project folder, with your venv active):
    python manage.py link_butterfly_maps
    python manage.py link_butterfly_maps --dry-run   (preview only, no writes)
"""
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from eonapp.models import Butterfly

MAP_DIR_REL = "Images/Butterfly_Maps"


class Command(BaseCommand):
    help = "Link existing Butterfly_Map_Image files to their Butterfly records by name."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without saving anything.",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Also replace a Butterfly_Map_Image that is already set (default: skip those).",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        overwrite = options["overwrite"]

        map_dir_abs = os.path.join(settings.MEDIA_ROOT, MAP_DIR_REL)
        if not os.path.isdir(map_dir_abs):
            self.stderr.write(self.style.ERROR(f"Map folder not found: {map_dir_abs}"))
            return

        # filename (without extension) -> actual filename on disk
        available = {}
        for fname in os.listdir(map_dir_abs):
            stem, ext = os.path.splitext(fname)
            if ext.lower() in (".webp", ".png", ".jpg", ".jpeg"):
                available[stem.lower()] = fname

        linked, skipped, missing = 0, 0, []

        for butterfly in Butterfly.objects.all():
            if butterfly.Butterfly_Map_Image and not overwrite:
                skipped += 1
                continue

            expected_stem = butterfly.Butterfly_Name.strip().replace(" ", "_").lower()
            fname = available.get(expected_stem)

            if not fname:
                missing.append(butterfly.Butterfly_Name)
                continue

            rel_path = f"{MAP_DIR_REL}/{fname}"
            self.stdout.write(f"{butterfly.Butterfly_Name!r} -> {rel_path}")

            if not dry_run:
                butterfly.Butterfly_Map_Image.name = rel_path
                butterfly.save(update_fields=["Butterfly_Map_Image"])
            linked += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nLinked: {linked}  Skipped (already set): {skipped}  "
            f"No matching file: {len(missing)}"
        ))
        if missing:
            self.stdout.write(self.style.WARNING(
                "No matching map image found for: " + ", ".join(missing)
            ))
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run — nothing was saved. Re-run without --dry-run to apply."))
