from django.shortcuts import render
from django.views import View
import MeCab
import re
from dataclasses import dataclass
from .models import Lecture, Course

def split_period_block(block: str):
    return list(map(int, re.findall(r"\d", block)))

 
def connect_period_block(list):
    i = 0
    results = []
    temp = list[0]
    for i in range(list[1]-list[0]+1):
        results.append(temp)
        temp = temp + 1
    
    return results

@dataclass
class Token:
    type: str
    value: any = None
    
DAY_RE = re.compile(r"(月|火|水|木|金|土)(?:曜|曜日)?")
PERIOD_RE = re.compile(r"\d((\s*(-|~|ー|～)\s*)\d)*")
LIMIT_RE = re.compile(r"限")
CONJ_RE = re.compile(r"(と|、|,|\s)")
SKIP_RE = re.compile(r"(の|は|に|で|を|も)")
    
def tokenize(text: str):
    token = []
    i = 0
    while i < len(text):
        chunk = text[i:]
        
        m = DAY_RE.match(chunk)
        if m:
            token.append(Token("DAY", m.group(1)))
            i = i + m.end()
            continue
            
        m = PERIOD_RE.match(chunk)
        if m:
            token.append(Token("PERIOD", m.group(0)))
            i = i + m.end()
            continue
            
        m = LIMIT_RE.match(chunk)
        if m:
            token.append(Token("LIMIT"))
            i = i + m.end()
            continue
            
        m = CONJ_RE.match(chunk)
        if m:
            token.append(Token("AND"))
            i = i + m.end()
            continue
            
        m = SKIP_RE.match(chunk)    
        if m:
            token.append(Token("SKIP"))
            i = i + m.end()
            continue
            
        i = i + 1
        
    return token

def parse_days_periods(prompt: str):
    tokens = tokenize(prompt)
    pairs = []
    
    current_days = []
    pending_periods = []
    state = "START"
    
    for tok in tokens:
        if tok.type == "DAY":
            if pending_periods:
                pending_periods.clear()
            if state == "EXPECTED_DAY":
                current_days.append(tok.value)
            else:
                current_days.append(tok.value)
            state = "EXPECTED_DAY"
        
        elif tok.type == "PERIOD":
            if re.match(r"\d\s*(?:-|~|ー|～)\s*\d", tok.value):
                result = connect_period_block(split_period_block(tok.value))
                pending_periods.extend(result)
            else:
                pending_periods.append(int(tok.value))
            state = "EXPECTED_LIMIT"
            
        elif tok.type == "LIMIT":
            if current_days and pending_periods:
                for c in current_days:
                    for p in pending_periods:
                        pairs.append((c,p))
            current_days.clear()
            pending_periods.clear()
            state = "START"
                        
        elif tok.type == "AND":
            continue
        
        elif tok.type =="SKIP":
            continue
        
        else:
            current_days.clear()
            pending_periods.clear()
            state == "START"
        
    return pairs
        
        
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
        
        pairs.extend(parse_days_periods(prompt))
        
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
                    if (d,p) not in pairs:
                        pairs.append((d,p))
                        
        print(pairs)
                
        years_match = re.search(r"(20\d{2})(?:年|年度)?",prompt)
        if years_match:
            years = int(years_match.group(1))
        reiwa_match = re.search(r"令和(\d+)", prompt)
        if reiwa_match:
            years = int(reiwa_match.group(1)) + 2018
        
        t=MeCab.Tagger("-Owakati")
        result = t.parse(prompt)
        List = result.split()
        print(List)
        all_items = Lecture.objects.all()
        return render(request, "Lecture_Search/index.html",{"pairs":pairs})
        
    
index = IndexView.as_view()
