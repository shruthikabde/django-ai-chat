import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import generate_hf_reply
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

@login_required
def chat_page(request):
    return render(request, 'chat.html')

@login_required
def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        msg = data.get('message', '')
        user = request.user
        username = user.first_name or user.username

        reply = generate_hf_reply(msg, username)
        return JsonResponse({'reply': reply})

    return JsonResponse({'error': 'Invalid request'}, status=400)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # user create avuthadu
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

