from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


def store(request):

    content = Product.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # total_cart_items = order.get_total_items
    else:
        items = []
        order = {'get_total_items': 0, 'get_cart_total': 0}

    return render(request, 'store/store.html', {"products": content, 'orders': order})


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_total_items': 0, 'get_cart_total': 0}

    context = {'items': items, 'orders': order}
    return render(request, 'store/cart.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_total_items': 0, 'get_cart_total': 0, 'shipping': False}

    context = {'orders': order, 'items': items}

    return render(request, 'store/checkout.html', context)


def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(productId)
    print(action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    productitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        productitem.quantity = productitem.quantity + 1
    elif action == 'remove':
        productitem.quantity = productitem.quantity - 1

    productitem.save()

    if productitem.quantity <= 0:
        productitem.delete()

    return JsonResponse('The data was sent', safe=False)
