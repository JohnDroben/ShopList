from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from yookassa import Webhook
import json
from .models import Order


@csrf_exempt
def yookassa_webhook(request):
    event_json = json.loads(request.body)

    try:
        # Проверяем подлинность уведомления
        webhook = Webhook(event_json)
        payment = webhook.object

        if payment.status == 'succeeded':
            # Обновляем статус заказа
            order_id = payment.description.split('#')[1]
            order = Order.objects.get(id=order_id)
            order.status = 'processing'
            order.save()

        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)