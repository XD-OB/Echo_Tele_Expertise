from django.shortcuts import render

def     dwv_display(request):
    return render(request, 'dwv/index.html', {})
