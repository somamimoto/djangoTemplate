from django.shortcuts import render


def home(request):
    if request.user.is_authenticated:
        context = {'user': request.user}
        return render(request, 'home.html', context)
    return render(request, 'home.html')
