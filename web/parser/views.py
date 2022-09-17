import time
import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.http import HttpResponse

from core.models import Car

from parser.parse.geely import geely_main
from parser.parse.haval import haval_main
from parser.parse.kia import KIA

kia = KIA()

PARSER_PATTERN = {
    "geely": geely_main,
    "haval": haval_main,
    "kia": kia.execute
}


def index(request):
    if not request.user.is_authenticated:
        # Return auth page
        return render(request, "parser/auth.html")
    else:
        # Return main page
        return redirect("profile")

def profile(request):
    session_key = request.COOKIES.get("sessionid")
    session = Session.objects.filter(session_key=session_key)
    if not session.exists():
        return redirect("auth")
    session = session.get()
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    cars = Car.objects.all()
    return render(request, "parser/profile.html", {
        "username": user.username, "full_name": user.get_full_name(),
        "is_superuser": user.is_superuser, "session_key": session_key,
        "cars": cars
    })

def auth(request):
    if request.user.is_authenticated:
        # Return main page
        return redirect("profile")

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("profile")
    else:
        data = {"message": "Неверные данные"}
        return render(request, "parser/auth.html", data)

def logout_view(request):
    logout(request)
    return redirect("index")

def run_parse(request):
    mark = request.POST.get("mark")
    _start_time = time.time()
    PARSER_PATTERN.get(mark)()
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60) 
    time_str = f"{t_hour}h:{t_min}m:{t_sec}s"
    return HttpResponse(json.dumps({"status": True, "time_string": time_str}), content_type='application/json')
