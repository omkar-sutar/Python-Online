from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
import time
from . import utilis
# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request,"pythoninterpreter/index.html")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data=json.loads(request.body.decode())
        code=data['code']
        input_=data['input']
        output=None
        try:
            output=utilis.execute_code(code,input_)
        except Exception as e:
            response={"output":"Internal server error"}
            print(e)
            return JsonResponse(response)
        response={"output":output}
        return JsonResponse(response)
       