from django.http import JsonResponse
from rest_framework.views import APIView


class HelloWorldView(APIView):
    
    def get(self, request):
        
        return JsonResponse(dict(
           status='OK',
           message='SUCCESS',
           data='Hello World'
        )) 
       
class HelloWorld2View(APIView):
    
    def get(self, request):        
        name = request.query_params.get('name', '')
        
        return JsonResponse(dict(
            status='OK',
            message='SUCCESS',
            data='Hello World {}'.format(name)
        )) 
