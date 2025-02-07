from django.shortcuts import render
from django.views import View

# Create your views here.
class HomepageView(View):
    def get(self, request):
        if request.method == 'GET':
            return render(request, "homepage-view-template.html")

    # def post(self, request):
    #     if request.method == 'POST':
    #
