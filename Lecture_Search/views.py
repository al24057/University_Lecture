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

class IndexView(View):
    def get(self, request):
        return render(request, "Lecture_Search/index.html")
    def post(self,request):
        prompt = request.POST.get("prompt")
        
        KANJI_NUM = {"一":"1", "二":"2", "三":"3", "四":"4", "五":"5", "六":"6",}
        
        for k,v in KANJI_NUM:
            prompt = prompt.replace(k,v)
        
        explict_pairs = re.findall(r"(月|火|水|木|金|土)(?:曜|曜日)?\s*(?:の)?\s*(\d+(?:\s*(?:[、,]|と|\s)\s*\d+)*)(?:時)?限", prompt)
        pairs = []
        periods = []
        for d,p in explict_pairs:
            temp = split_period_block(p)
            for t in temp:
                pairs.append((d,t))
                
        implict_pairs = re.findall(r"(月|火|水|木|金|土)(?:曜|曜日)?\s*(?:の)?\s*(\d+(?:\s*(?:[、,]|と|\s)\s*\d+)*)", prompt)
        if not pairs:
            for d,p in implict_pairs:
                temp = split_period_block(p)
                for t in temp:
                    pairs.append((d,t))
                    
        days_match = re.findall(r"(月|火|水|木|金|土)(?:曜|曜日)?", prompt)
        periods_match = re.findall(r"(\d+(?:\s*(?:[、,]|\s)\s*\d+)*)(?:時)?限", prompt)
        if pairs and periods_match:
            used_pairs = set(pairs)
            last_day = pairs[-1][0]
            for pm in periods_match:
                for p in split_period_block(pm):
                    if not ((last_day,p) in used_pairs):
                        pairs.append((last_day, p))
                        used_pairs.add((last_day, p))
                        
        if days_match and periods_match:
            expected = len(set(days_match)) * len(set(p for pm in periods_match for p in split_period_block(pm)))

            if len(pairs) < expected:
                all_days = list(dict.fromkeys(days_match))
                all_periods = []
                for pm in periods_match:
                    all_periods.extend(split_period_block(pm))
                all_periods = list(dict.fromkeys(all_periods))

                for d in all_days:
                    for p in all_periods:
                        if (d, p) not in pairs:
                            pairs.append((d, p))
                
        
        for d in periods_match:
            periods.extend(split_period_block(d))
        
        t=MeCab.Taggar()
        result = t.parse(prompt)
        
    
index = IndexView.as_view()
