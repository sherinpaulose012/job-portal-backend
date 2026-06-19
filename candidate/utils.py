# candidate/utils.py

import os
from datetime import datetime

def resume_upload_path(instance, filename):

    extension = filename.split('.')[-1]

    new_filename = (
        f"candidate_{instance.user.id}_"
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        f".{extension}"
    )

    return os.path.join(
        'resumes',
        new_filename
    )
