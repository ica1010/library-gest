from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from library_prj.users.models import User
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def user_detail_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    return render(request, "users/user_detail.html", {"user": user_obj})

@login_required
def user_update_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            request.user.name = name
            request.user.save()
            messages.success(request, "Information successfully updated")
            return redirect(request.user.get_absolute_url())
    return render(request, "users/user_form.html", {"user": request.user})

@login_required
def user_redirect_view(request):
    return redirect("users:dashboard")

@login_required
def user_profile(request):
    return render(request, "users/profile.html", {"user": request.user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()
        messages.success(request, "Profil mis à jour avec succès.")
        return redirect("users:profile")
    return render(request, "users/edit_profile.html", {"user": user})

def dire_bonjour(nom):
    return f"Bonjour, {nom} !"

@staff_member_required
def admin_user_list_view(request):
    users = User.objects.all()
    return render(request, "admin/user_list.html", {"users": users})
