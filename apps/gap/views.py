from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate

from apps.gap.models import Room, Opinion, Comment, OpinionLike


class RoomListView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'gap/rooms.html', {"rooms": rooms})


class RoomDetailView(View):
    def get(self, request, pk):
        room = Room.objects.get(pk=pk)

        opinions = sorted(Opinion.objects.filter(room=room), key=lambda o: o.like_count, reverse=True)
        context = {
            "room": room,
            "opinions": opinions
        }
        return render(request, "gap/opinoins.html", context=context)


class LikeOpinionView(View):
    def get(self, request, pk):
        opinion = Opinion.objects.get(pk=pk)
        like, created = OpinionLike.objects.get_or_create(user=request.user, opinion=opinion)
        if not created:
            like.delete()
        return redirect(reverse("gap:room", kwargs={"pk": opinion.room.pk}))


class OpinionDetailView(View):
    def get(self, request, pk):
        opinion = Opinion.objects.get(pk=pk)
        comments = opinion.comments.all().order_by("-created_at")
        context = {
            "opinion": opinion,
            "comments": comments
        }
        return render(request, "gap/comments.html", context=context)


# class LoginPageView(LoginView):
#     template_name = 'login.html'
#
#
# class RegisterPageView(CreateView):
#     template_name = 'register.html'
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login-page')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gap:rooms')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('gap:rooms')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
