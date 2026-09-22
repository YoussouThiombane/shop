from functools import wraps

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


def owner_required(view_func):
    """Protect an owner view and prevent browser/proxy caching."""
    protected = login_required(never_cache(view_func))

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = protected(request, *args, **kwargs)
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response

    return wrapper
