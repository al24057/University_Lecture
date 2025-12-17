from django.shortcuts import render
from django.views import View
import MeCab
import re
# Create your views here.

def split_period_block(block: str):
    result = []

    block = block.replace(" ","").replace("　","").replace(",","").replace("、","").replace("と","")

    if len(block) == 1:
        result.append(int(block))

    elif len(block) >= 2:
        for d in block:
            temp = int(d)
            result.append(temp)

    return result

def connect_period_block(block: str):
    result = []
    
    block = block.replace("-","").replace("ー","").replace("~","").replace("～","").replace("から","")
    
    if len(block) == 1:
        result.append(int(block))

    elif len(block) >= 2:
        for d in block:
            temp = int(d)
            result.append(temp)
            
    r = result[0]
    new_result = []
    while(r <= result[len(result-1)]):
        new_result.append(r)
        r = r + 1
        
    return new_result

class IndexView(View):
    def get(self, request):
        return render(request, "Lecture_Search/index.html")
    def post(self,request):
        prompt = request.POST.get("prompt")
        
        if (re.search(r"(一|二|三|四|五|六)", prompt)):
            KANJI_NUM = {"一":"1", "二":"2", "三":"3", "四":"4", "五":"5", "六":"6",}
        
            for k,v in KANJI_NUM.items():
                prompt = prompt.replace(k,v)
                
        pairs = []
        blocks = re.findall(r".*?\d(?:\s*(?:[、,]|と|\s)\s*\d)*\s*限", prompt)
        prev_days = []
        
        for b in blocks:        
            days = re.findall(r"(月|火|水|木|金|土)(?:曜|曜日)?", b)
            periods = re.findall(r"(\d+(?:\s*(?:[、,]|と|\s)\s*\d+)*)(?:時)?限",b)
            results = []
            
            for p in periods:
                results.extend(split_period_block(p))
                
            if days:
                use_days = days
                prev_days = days
            else:
                use_days = prev_days
            
            for d in use_days:
                for p in results:
                    pairs.append((d,p))
                
        years_match = re.search(r"(20\d{2})(?:年|年度)?",prompt)
        if years_match:
            years = int(years_match.group(1))
        reiwa_match = re.search(r"令和(\d+)", prompt)
        if reiwa_match:
            years = int(reiwa_match.group(1)) + 2018
            
        
        
        #t=MeCab.Taggar()
        #result = t.parse(prompt)
        return render(request, "Lecture_Search/index.html",{"pairs":pairs})
        
    
index = IndexView.as_view()
