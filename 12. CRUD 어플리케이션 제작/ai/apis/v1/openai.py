import requests
from django.http import JsonResponse
from rest_framework.views import APIView

from ai.models import OpenaiMessage
from project import settings


class OpenaiMessageView(APIView):

    def get(self, request):
        pre_message_count = int(request.query_params.get('pre_message_count', 10))

        message_queryset = OpenaiMessage.objects.order_by('-created_at').values_list('message', flat=True)[:pre_message_count]
        message_queryset = list(message_queryset)
        message_queryset.reverse()

        message_list = list()
        temp = ["", ""]
        for index in range(0, pre_message_count):
            c = message_queryset[index]
            temp[index % 2] = c

            if index % 2 == 1:
                message_list.append(temp)
                temp = ["", ""]

        return JsonResponse(dict(status="OK", message="데이터를 조회하였습니다.", datas=message_list))

    def post(self, request):
        message = request.data.get('message')
        pre_message_count = int(request.data.get('pre_message_count', 10))

        message_queryset = OpenaiMessage.objects.order_by('-created_at')[:pre_message_count]

        message_list = list()

        for c in message_queryset:
            message_list.append(dict(
                role="assistant",
                content=c.message
            ))

        # 메시지를 포함하는 요청 데이터를 만들어야 한다.
        message_list.append(dict(
            role="user",
            content=message
        ))

        payload = dict(
            messages=message_list,
            temperature=0.8,
            top_p=0.7,
            max_tokens=800
        )

        # API KEY를 포함하는 헤더를 만들고,
        headers = {
            'Content-Type': 'application/json',
            'api-key': settings.AZURE_OPENAI_API_KEY
        }

        OpenaiMessage.objects.create(message=message)

        response = requests.post(settings.AZURE_OPENAI_ENDPOINT,
                                 headers=headers,
                                 json=payload)

        # 예외처리.
        if response.status_code == 200:
            response_json = response.json()
            response_content = response_json['choices'][0]['message']['content']
            # 리턴받은 컨텐츠를 데이터베이스에 저장.
            # OpenaiMessage.objects.bulk_create([OpenaiMessage(message=message)])
            OpenaiMessage.objects.create(message=response_content)
            return JsonResponse(dict(status="OK", message="요청을 성공하였습니다.", data=response_content))
        else:
            return JsonResponse(dict(status="REQUEST_FAILED", message="요청에 실패하였습니다.", data=""), status=400)
