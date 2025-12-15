from django.shortcuts import render
from django.views import View
import MeCab
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, "Lecture_Search/index.html")
    def post(self,request):
        prompt = request.POST.get("prompt")
        t=MeCab.Taggar()
        result = t.parse(prompt)
        曜日マップ = {"月曜":0, "火曜":1, "水曜":2, "木曜":3, "金曜":4, "土曜":5, "日曜":6}
    
index = IndexView.as_view()
