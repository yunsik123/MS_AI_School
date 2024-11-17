from django.urls import path

from ai.apis.v1.openai import OpenaiMessageView

urlpatterns = [
    path('messages/', OpenaiMessageView.as_view(), name='openaiMessage')
]