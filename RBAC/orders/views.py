import requests
import json
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from .serializers import *
from .models import *
from .email import send_html_email
from .push import send_push_message
from django.core.mail import send_mail as sm
from django.http import HttpResponse, JsonResponse
from common.pagination import CustomPagination

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    permission_classes =[AllowAny]
  
class ItemViewset(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer 
    pagination_class = CustomPagination
    permission_classes =[AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','name', 'desc']
    ordering_fields = ['id','name', 'desc']
    search_fields = ['id','name', 'desc']

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@csrf_exempt
def accept_shipment(request, id):
    data = request.data
    print(data['taskBody']['shipmentAccepted'])
    shipment_val = data['taskBody']['shipmentAccepted']
    try:
        if(shipment_val):
            details = {'status':'Shipment Accepted'}
            order = Order.objects.get(pk=id)
            serializer = OrderSerializer(order, data=details, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data, safe=False)   
    except:
        return HttpResponse(status=400)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@csrf_exempt
def print_pick_list(request, id):
    data = request.data
    try:
        details = {'status':'Pick List Printed'}
        order = Order.objects.get(pk=id)
        serializer = OrderSerializer(order, data=details, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, safe=False)     
    except:
        return HttpResponse(status=400)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@csrf_exempt
def validate_stock(request, id):
    data = request.data
    stock_val = data['taskBody']['stockLevel']
    order = Order.objects.filter(pk=id).first()
    orderType = order.orderType
    print(orderType)
    context = { 
        'enRoute': f"http://192.168.1.68:8000/orders/api/commerce/shipments/{order.pk}/canceled",
        'curbside' : f"http://192.168.1.68:8000/orders/api/commerce/shipments/{order.pk}/customerAtCurbside"
        }
    try:
        if(orderType == 'Bopis'):
            if(stock_val == 'IN_STOCK'):
                details = {'status':'Stock Validated'}
                serializer = OrderSerializer(order, data=details, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse(serializer.data, safe=False)
        elif(orderType == 'Curbside'):
            if(stock_val == 'IN_STOCK'):
                details = {'status':'Stock Validated'}
                serializer = OrderSerializer(order, data=details, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                res = send_html_email(['aking@everesttech.com', 'aking893.ak@gmail.com'],
                                f'Order #: {order.orderID}', 'orders/enroute.html', context, f"{settings.EMAIL_FROM_ADDRESS}")
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponse(status=400)
    except:
        return HttpResponse(status=400)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@csrf_exempt
def customer_accepted(request, id):
    data = request.data
    customer_val = data['taskBody']['customerAccepted']
    try:
        if(customer_val):
            details = {'status':'Complete'}
            order = Order.objects.get(pk=id)
            serializer = OrderSerializer(order, data=details, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data, safe=False)        
    except:
        return HttpResponse(status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def customer_en_route(request, id):
    data = request.data
    order = Order.objects.filter(pk=id).first()
    token = order.pushToken
    url = 'http://localhost:19002/api/v2/push/send'
    message = {
        'to': token,
        'sound': 'default',
        'title': 'En Route',
        'body': f'Customer with Order# {order.orderID} is {order.status}.',
    }
    converted = json.dumps(message)
    try:
        details = {'status':'Customer En Route'}
        serializer = OrderSerializer(order, data=details, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # if(token == order.pushToken):
        #     x = requests.post(url, data = converted)
        #     return HttpResponse(status=200)
        # else:
        #     return HttpResponse(status=204)  
    except:
        return HttpResponse(status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def customer_curbside(request, id):
    data = request.data
    order = Order.objects.filter(pk=id).first()
    token = order.pushToken
    url = 'http://localhost:19002/api/v2/push/send'
    message = {
        'to': token,
        'sound': 'default',
        'title': 'En Route',
        'body': f'Customer with Order# {order.orderID} is {order.status}.',
    }
    converted = json.dumps(message)
    try:
        details = {'status':'Customer Curbside'}
        serializer = OrderSerializer(order, data=details, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # if(token == order.pushToken):
        #     x = requests.post(url, data = converted)
        #     return HttpResponse(status=200)
        # else:
        #     return HttpResponse(status=204)
    except:
        return HttpResponse(status=400)

@api_view(['GET','PUT', 'PATCH'])
@permission_classes([AllowAny])
@csrf_exempt
def register_push_notifications(request, id):
    data = request.data
    order = Order.objects.filter(pk=id).first()
    token = data['pushToken']
    try:
        details = {'pushToken': token}
        serializer = OrderSerializer(order, data=details, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponse(status=200)       
    except:
        return HttpResponse(status=400)