from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
import json


def index(request):
    labels = ["jan", "feb", "mar", "apr"]
    data = [100, 80, 300, 200]
    context = {"collapse": "",
               "labels": json.dumps(labels),
               "data": json.dumps(data), }
    return render(request, "dashboard.html", context)

