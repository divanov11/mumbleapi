import os
from datetime import datetime

def profile_pic_location(profile, filename):
    path = os.path.join("Mumble Profile Pictures", profile.username, str(datetime.now().date().strftime("%d, %B, %Y")), filename)
    return path