from django.shortcuts import render

# Create your views here.
from scripts.xinlang import *
from scripts.duowan import *
from scripts.hupu import *
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

def xinlang(request):


    ps = request.GET.get("ps", None)
    pn = request.GET.get("pn", None)

    print(ps,pn)

    if ps is None or pn is None:

        re_json = {"succ": True,  "data": []}

        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')

        #return HttpResponse("参数错误", content_type='application/json',charset='utf-8')
    try:

        print(get_xinlang(ps, pn))

        re_json = {"succ": False, "data": get_xinlang(ps,pn)}



        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')
    except:

        re_json = {"succ": False, "data": []}
        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')

def duowan(request):


    ps = request.GET.get("ps", None)
    pn = request.GET.get("pn", None)

    print(ps,pn)

    if ps is None or pn is None:

        re_json = {"succ": False,  "data": []}

        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')

        #return HttpResponse("参数错误", content_type='application/json',charset='utf-8')
    try:

        print(get_duowan(ps, pn))

        re_json = {"succ": True, "data": get_duowan(ps,pn)}



        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')
    except:

        re_json = {"succ": False, "data": []}
        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')



def hupu(request):


    ps = request.GET.get("ps", None)
    pn = request.GET.get("pn", None)

    print(ps,pn)

    if ps is None or pn is None:

        re_json = {"succ": False,  "data": []}

        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')

        #return HttpResponse("参数错误", content_type='application/json',charset='utf-8')
    try:

        #print(get_hupu(ps, pn))

        re_json = {"succ": True, "data": get_hupu(ps,pn)}



        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')
    except:

        re_json = {"succ": False, "data": []}
        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')
