from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = AuthenticationForm(request, data=request.POST or None)
    for field in form.fields.values():
        field.widget.attrs.setdefault("class", "form-control")
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Bienvenue dans votre espace propriétaire.")
        candidate = request.POST.get("next") or request.GET.get("next")
        next_url = candidate if candidate and url_has_allowed_host_and_scheme(candidate, {request.get_host()}) else None
        return redirect(next_url or "dashboard:home")
    return render(request, "accounts/login.html", {"form": form, "next": request.GET.get("next", "")})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes maintenant déconnecté.")
    response = redirect("accounts:login")
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response
