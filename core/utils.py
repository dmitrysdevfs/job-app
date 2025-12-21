import uuid
from pathlib import Path
from django.db import models
from django.utils.text import slugify


def upload_to(instance: models.Model, filename: str, folder_name: str) -> str:
    """Return the upload path for files with unique UUID and slugified name."""
    path = Path(filename)
    unique_filename = f"{slugify(path.stem)}_{uuid.uuid4().hex[:8]}{path.suffix}"
    return str(Path(folder_name) / unique_filename)
