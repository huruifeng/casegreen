import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.

def index(request):
    return render(request,'mycase/index.html')

def mycase(request):
    if request.method == "GET":
        return render(request,'mycase/index.html')
    elif request.method == "POST":
        return render(request,'mycase/mycase.html')

def visabulletin(request):
    if request.method == "GET":
        return render(request,'mycase/visabulletin.html')
    elif request.method == "POST":
        return render(request,'mycase/visabulletin.html')

def getjson(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the data_type from the client side.
        data_type = request.GET.get("data_type", None)
        # check for the data_type.
        if data_type=="lollipop":
            data_dict = {}
            with open("mycase/data/O14976_mutation.txt","r") as f:
                mut_str = f.read()
            with open("mycase/data/O14976_domain.txt","r") as f:
                domain_str = f.read()
            data_dict['mut_sites'] = mut_str
            data_dict['domains'] = domain_str
            return HttpResponse(json.dumps(data_dict), status=200)
        else:
            return JsonResponse({}, status=200)

    return JsonResponse({}, status=400)

