from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum, FloatField

from .models import ItemType, Item, Order, OrderItem, Topping, TMP_ID, Size

def get_order(request):
    # тут надо добавить проверку на статус заказа, так как
    #  кроме факта наличия заказа с ИД пользователя, еще не значит, что это тот самый заказа
    # мы ж структуру базы изменили и теперь все заказы в одной таблице
    user_for_order = get_user(request)
    order_record, created = Order.objects.filter(user_id=user_for_order).get_or_create(user_id=user_for_order)
    return order_record

def get_user(request):
    if request.user.is_authenticated:
        return str(request.user.pk)
    else:
        # не проверяем, так как
        # в принципе такой ситуации не может быть, что юзер запустил добавление
        # заказа, и при этом ему не был назначени user_id
        if request.method == "POST":
            return request.POST["user_id"]
        else:
            return request.session['user_id']

def remove_item_from_cart_view(request):
    if request.is_ajax and request.method == "POST":
        item_id = int(request.POST['item_id'])
        order_id = int(request.POST['order_id'])
        z = OrderItem.objects.filter(pk=item_id).delete()
        order = Order.objects.get(order_id=order_id)
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
    pass

def add_to_cart_view(request):
    if request.is_ajax and request.method == "POST":
        try:
            item_pk = int(request.POST["item_pk"])
            add_item = Item.objects.get(pk=item_pk)
        except KeyError:
            return render(request, "orders/error.html", {"message": "No selection"})
        except Item.DoesNotExist:
            return render(request, "orders/error.html", {"message": "No item"})

        new_order = get_order(request)

        new_order_item = OrderItem(item = add_item, itemPrice = request.POST["price"], itemSize =  Size.objects.get(pk=int(request.POST["size"])), user_id =get_user(request), order_id = new_order)
        new_order_item.save()
        if 'order_id' not in request.session:
            request.session['order_id'] = new_order.order_id
        summm = OrderItem.objects.filter(order_id=new_order).aggregate(Sum('itemPrice', output_field=FloatField()))['itemPrice__sum']
        new_order.total = summm
        new_order.save()
        a = {   "order_id": new_order.order_id,
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

def index(request):
    allpizza = {
        "Regular Pizza"  : Item.objects.filter(itemtype__name='Regular Pizza'),
        "Sicilian Pizza" : Item.objects.filter(itemtype__name='Sicilian Pizza'),
        "Subs"           : Item.objects.filter(itemtype__name='Subs').order_by('name'),
        "Dinner Platters": Item.objects.filter(itemtype__name='Dinner Platters').order_by('name')
    }
    s_p = {
        "Pasta"           : Item.objects.filter(itemtype__name='Pasta').order_by('name'),
        "Salads": Item.objects.filter(itemtype__name='Salads').order_by('name')
    }

    context = {
        "items"         : Item.objects.all(),
        "allpizza"      : allpizza,
        "salads_pasta"  : s_p,
        "pizza_topings" : Topping.objects.filter(itemtype__name='Toppings (pizza)').order_by('name')
    }

    if not request.user.is_authenticated:
        context['user'] = 'none'
        if 'user_id' not in request.session:
            request.session['user_id'] = TMP_ID()
    else:
        context['user'] = request.user
    context['user_id'] = request.session['user_id']

    if 'order_id' in request.session:
        c_order = get_order(request)
        context['total'] = c_order.total
        context['current_order_list'] = OrderItem.objects.filter(order_id=c_order)
    return render(request, "orders/index.html", context)

def cabinet_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
            "user": request.user
        }
        return render(request, "orders/cabinet.html", context)

def signin_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "index", {"message": "Problem with signing up."})

def logout_view(request):
    del request.session['user_id']
    logout(request)
    return HttpResponseRedirect(reverse ("index"))
