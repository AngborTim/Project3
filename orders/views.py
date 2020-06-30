from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum, FloatField
import json

from .models import ItemType, Item, Order, OrderItem, OrderStatus, Topping, Size #TMP_ID,

def get_order(request, address, type, id):
    # если мы добрались до создания или получения заказа, то session['user_id']
    # должен по-любому существовать
    user_for_order = request.session['user_id']
    if address == "show":
        if type == "basket":
            try:
                order_record = Order.objects.get(user_id=user_for_order, order_status__orderType='In basket')
            except:
                order_record = 'nill'
        if type == "all":
            order_record = Order.objects.filter(user_id=user_for_order)
        if type == "one":
            order_record = Order.objects.get(pk=id)
    if address == "add" and type == "basket":
    # создаем или получаем заказ-корзину user_id
        order_record, created = Order.objects.filter(user_id=user_for_order).get_or_create(user_id=user_for_order, order_status__orderType='In basket')
        if 'order_id' not in request.session:
            request.session['order_id'] = order_record.pk

    return order_record


def remove_item_from_cart_view(request):
    if request.is_ajax and request.method == "POST":
        item_id = int(request.POST['item_id'])
        order_id = int(request.POST['order_id'])
        z = OrderItem.objects.filter(pk=item_id).delete()
        order = Order.objects.get(pk=order_id)
        if OrderItem.objects.filter(order_id=order):
            summm = OrderItem.objects.filter(order_id=order).aggregate(Sum('itemPrice', output_field=FloatField()))['itemPrice__sum']
        else:
            summm = 0
        order.total = summm
        order.save()
        return JsonResponse({"total": summm, "status":"OK"}, status=200)
    else:
        return JsonResponse({"error": "BOO"}, status=400)

def add_topings_view(request):
    if request.is_ajax and request.method == "POST":
        try:
            topping_pk_array = request.POST["topping_pk_array"]
            order_item_pk = int(request.POST["order_item_pk"])
            order_item = OrderItem.objects.get(pk=order_item_pk)
            order_item.order_id.total -= order_item.topings_totall
            order_item.order_id.save()
            order_item.topping.clear()
        except KeyError:
            return render(request, "orders/error.html", {"message": "No selection"})
        except OrderItem.DoesNotExist:
            return render(request, "orders/error.html", {"message": "No order item"})
        except Topping.DoesNotExist:
            return render(request, "orders/error.html", {"message": "No topping item"})

        a = json.loads(topping_pk_array)
        for val in a.values():
            if val != 'null':
                topping = Topping.objects.get(pk=int(val))
                order_item.topping.add(topping)
        order_item.order_id.total += order_item.topings_totall
        order_item.order_id.save()

        return JsonResponse({"status":"OK", "total_order": order_item.order_id.total, "total_item": order_item.totall_price, "item_pk" : order_item_pk}, status=200)

def add_to_cart_view(request):
    if request.is_ajax and request.method == "POST":
        try:
            item_pk = int(request.POST["item_pk"])
            add_item = Item.objects.get(pk=item_pk)
        except KeyError:
            return render(request, "orders/error.html", {"message": "No selection"})
        except Item.DoesNotExist:
            return render(request, "orders/error.html", {"message": "No item"})

        #создаем или получаем текущий заказ-корзину
        new_order = get_order(request, 'add', 'basket', 'nill')

        new_order_item = OrderItem(item = add_item, itemPrice = request.POST["price"], itemSize =  Size.objects.get(pk=int(request.POST["size"])), user_id =request.session['user_id'], order_id = new_order)
        new_order_item.save()

        summm = OrderItem.objects.filter(order_id=new_order).aggregate(Sum('itemPrice', output_field=FloatField()))['itemPrice__sum']
        new_order.total = summm
        new_order.save()
        a = {   "order_id": new_order.pk,
                "item_id" : new_order_item.pk,
                "type"    : add_item.itemtype.name,
                "name"    : add_item.name,
                "extratop": add_item.has_extra_toppings,
                "size"    : Size.objects.get(pk=int(request.POST["size"])).sizeName,
                "price"   : request.POST['price'],
                "total"   : new_order.total
            }

        if add_item.itemtype.name == "Regular Pizza" or add_item.itemtype.name == "Sicilian Pizza":
            topings = Topping.objects.filter(itemtype__name='Toppings (pizza)').values("pk", "itemtype__name", "name", "price").order_by('name')
        elif add_item.itemtype.name == "Subs" and add_item.name != "Steak + Cheese":
            topings = Topping.objects.filter(itemtype__name='Extra for subs').values("pk", "itemtype__name", "name", "price")
        elif add_item.name == "Steak + Cheese":
            topings = Topping.objects.filter(itemtype__name__in=['Extra for subs','Extra for Steak + Cheese']).values("pk", "itemtype__name", "name", "price").order_by('name')
        else:
            topings = {'toppings': 'none'}

        return JsonResponse({"result": a, "toppings": list(topings), "status":"OK"}, status=200)
    else:
        return JsonResponse({"error": "BOO"}, status=400)



def allpizza():
    allpizza = {
        "Regular Pizza"  : Item.objects.filter(itemtype__name='Regular Pizza'),
        "Sicilian Pizza" : Item.objects.filter(itemtype__name='Sicilian Pizza'),
        "Subs"           : Item.objects.filter(itemtype__name='Subs').order_by('name'),
        "Dinner Platters": Item.objects.filter(itemtype__name='Dinner Platters').order_by('name')
    }
    return allpizza

def s_p():
    s_p = {
        "Pasta"   : Item.objects.filter(itemtype__name='Pasta').order_by('name'),
        "Salads"  : Item.objects.filter(itemtype__name='Salads').order_by('name')
    }
    return s_p

def index(request):
    if not request.user.is_authenticated:
        context = {'user': 'none'}
        return render(request, "orders/login.html", context)
    else:
        user_id = request.user.id
        request.session['user_id'] = user_id

    context = {
        "items"           : Item.objects.all(),
        "allpizza"        : allpizza(),
        "salads_pasta"    : s_p(),
        "pizza_toppings"  : Topping.objects.filter(itemtype__name='Toppings (pizza)').values("pk", "itemtype__name", "name", "price").order_by('name'),
        "subs_toppings"   : Topping.objects.filter(itemtype__name='Extra for subs').values("pk", "itemtype__name", "name", "price"),
        "steak_and_cheese": Topping.objects.filter(itemtype__name__in=['Extra for subs','Extra for Steak + Cheese']).values("pk", "itemtype__name", "name", "price").order_by('name'),
        "user"            : request.user
        }

    if 'order_id' in request.session:
        # если заказ-корзина начал формироваться то передаем его
        # в index
        # заказ создается при добавлении первого пункта заказа в функции add_to_cart_view
        c_order = get_order(request, 'show', 'basket', 'nill')
        if c_order != 'nill':
            context['total'] = c_order.total
            context['order'] = c_order
            context['current_order_list'] = OrderItem.objects.filter(order_id=c_order)

    return render(request, "orders/index.html", context)

def cabinet_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
            "user"              : request.user,
            "pizza_toppings"    : Topping.objects.filter(itemtype__name='Toppings (pizza)').values("pk", "itemtype__name", "name", "price").order_by('name'),
            "subs_toppings"     : Topping.objects.filter(itemtype__name='Extra for subs').values("pk", "itemtype__name", "name", "price"),
            "steak_and_cheese"  : Topping.objects.filter(itemtype__name__in=['Extra for subs','Extra for Steak + Cheese']).values("pk", "itemtype__name", "name", "price").order_by('name')
        }

        all_orders = get_order(request, 'show', 'all', 'nill')
        context['all_orders'] = all_orders
        basket = get_order(request, 'show', 'basket', 'nill')
        if basket != 'nill':
            context['basket'] = basket
            context['current_order_list'] =  OrderItem.objects.filter(order_id=basket)

        if request.user.is_staff:
            all_users_orders = Order.objects.all()
            context['all_users_orders'] = all_users_orders

        return render(request, "orders/cabinet.html", context)

def order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return HttpResponseRedirect(reverse("cabinet"))
    context = {
        "order": order,
        "items": OrderItem.objects.filter(order_id=order)
        }
    if request.user.is_staff:
        order_status = OrderStatus.objects.all()
        context['order_status'] = order_status
    return render(request, "orders/order.html", context)


def order_placing_view(request):
    order = get_order(request, 'show', 'basket', 'nill')

    if order.order_status.orderType == 'In basket':
        new_type = OrderStatus.objects.get(orderType='Placed')
        order.order_status = new_type
        order.save()
    del request.session['order_id']

    return HttpResponseRedirect(reverse("cabinet"))

def change_order_status_view(request):
    try:
        id = int(request.POST['order_id'])
        new_status = int(request.POST['new_status'])
        order = get_order(request, 'show', 'one', id)
        new_type = OrderStatus.objects.get(pk=new_status)
        order.order_status = new_type
        order.save()
        return JsonResponse({"status":"OK", "new_status": new_type.orderType}, status=200)
    except:
        return JsonResponse({"status":"TROUBLES"}, status=400)

def delete_order_view(request):
    try:
        id = int(request.POST['order_id'])
        order = get_order(request, 'show', 'one', id)
        order.delete()
        return JsonResponse({"status":"OK", "was_deleted_id": id}, status=200)
    except:
        return JsonResponse({"status":"TROUBLES"}, status=400)


def signin_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        request.session['user_id'] = user.id
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "index", {"message": "Invalid credentials."})

def signup_view(request):
    username = request.POST["username"]
    email    = request.POST["email"]
    password = request.POST["password"]
    first    = request.POST["first"]
    last     = request.POST["last"]

    user = User.objects.create_user(username, email, password)
    user.last_name = last
    user.first_name = first
    user.save()
    if user is not None:
        login(request, user)
        request.session['user_id'] = user.id
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "index", {"message": "Problem with signing up."})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse ("index"))
