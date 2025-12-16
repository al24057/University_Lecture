from django.shortcuts import render
from django.views import View
import MeCab
import re
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, "Lecture_Search/index.html")
    def post(self,request):
        prompt = request.POST.get("prompt")
        
        KANJI_NUM = {"一":"1", "二":"2", "三":"3", "四":"4", "五":"5", "六":"6",}
        
        for k,v in KANJI_NUM:
            prompt = prompt.replace(k,v)
        
        match = re.findall(r"(月|火|水|木|金|土)(?:曜|曜日)?\s*(?:の)?\s*(\d+(?:\s*[、,]\s*\d+)*)(?:時)?限", prompt)
        days_match = re.findall(r"(月|火|水|木|金|土)(?:曜|曜日)?", prompt)
        periods_match = re.findall(r"(\d|一|二|三|四|五|六)(?:時)?限", prompt)

        
        t=MeCab.Taggar()
        result = t.parse(prompt)
        曜日マップ = {"月曜":0, "火曜":1, "水曜":2, "木曜":3, "金曜":4, "土曜":5}
    
index = IndexView.as_view()
