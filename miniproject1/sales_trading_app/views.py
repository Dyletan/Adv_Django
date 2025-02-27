from django.shortcuts import render

def index_view(request):
    """
    View for the home page (index page).
    Renders the 'index.html' template.
    """
    return render(request, 'index.html')