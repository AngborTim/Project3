from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import ItemType, Item, Order, TmpOrder, OrderItem, Toppings, TMP_ID

def add_to_cart_view(request):
    if request.is_ajax and request.method == "POST":
        try:
            item_pk = int(request.POST["item_pk"])
            add_item = Item.objects.get(pk=item_pk)
        except KeyError:
            return render(request, "orders/error.html", {"message": "No selection"})
        except Item.DoesNotExist:
            return render(request, "orders/error.html", {"message": "No item"})
        if request.user.is_authenticated:
            useridfororder = str(request.user.pk)
        else:
            useridfororder = request.POST["temp_id"]
        if not TmpOrder.objects.filter(user_id=useridfororder):
            tmp_order_record = TmpOrder(user_id = useridfororder)
            tmp_order_record.save()
        else:
            tmp_order_record = TmpOrder.objects.get(user_id=useridfororder)
        new_order_item = OrderItem(item = add_item, itemPrice = request.POST["price"], itemSize =  request.POST["size"], user_id =useridfororder, order_id = tmp_order_record)
        new_order_item.save()
        a = {   "type": add_item.itemtype.name,
                "name": add_item.name,
                "extratop": add_item.has_extra_toppings,
                "size": request.POST['size'],
                "price": request.POST['price']
            }

        return JsonResponse({"result": a, "status":"OK"}, status=200)
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
        "items"        : Item.objects.all(),
        "allpizza"     : allpizza,
        "salads_pasta" : s_p
    }
    if not request.user.is_authenticated:
        context['user'] = 'none'
    else:
        context['user'] = request.user

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
    logout(request)
    return HttpResponseRedirect(reverse ("index"))
