from django.urls import path
from ai.apis.v1.common import HelloWorldView, HelloWorld2View

urlpatterns = [
    path('helloworld/', HelloWorldView.as_view(), name='helloWorld'),
    path('helloworld2/', HelloWorld2View.as_view(), name='helloWorld2')
]
