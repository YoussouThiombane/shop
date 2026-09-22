from django.db.utils import OperationalError, ProgrammingError

from .models import SiteSettings


def site_settings(request):
    try:
        settings = SiteSettings.get_solo()
    except (OperationalError, ProgrammingError):
        settings = SiteSettings()
    return {"site_settings": settings}
