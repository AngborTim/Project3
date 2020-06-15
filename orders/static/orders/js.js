document.addEventListener('DOMContentLoaded', function(){
add_deletion();
add_menu();

var hh = window.innerHeight - document.getElementById('foo').clientHeight - document.getElementById('nav').clientHeight - document.getElementById('extra_nav').clientHeight  + 'px';
 $('#scrl').css('height', hh);
 $('#order_list').css('height', hh, 'important');

if (document.querySelector('#signup_btn')){
    signup_click();
    signup_submit();
  }
if (document.querySelector('#user_account')){
    logout();
    account_popover();
  }
});


function deletion(elm){

  elm.addEventListener("click", function(){
     var to_delete = document.querySelector('#item-'+elm.dataset.item_id);
     to_delete.style.animationPlayState = 'running';
     to_delete.addEventListener('animationend', () =>  {
       to_delete.remove();
     });
     var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
     $.post(remove_item_from_cart, {
       item_id: elm.dataset.item_id,
       user_id: elm.dataset.user_id,
       order_id: elm.dataset.order_id,
       csrfmiddlewaretoken: csrftoken },
       function(){
         document.querySelector('.spinner-border').classList.remove('d-none');
         document.querySelector('main').setAttribute( 'style', 'position: fixed; opacity:50% !important');
       })
       .done(function( data ) {
         // все получилось
         if (data['status'] == "OK"){
           if (data['total'] != 0 ){
              document.getElementById('total').innerHTML = ' Total: $' + data['total'].toFixed(2);
           }
           else{
             document.getElementById('total').innerHTML = 'Cart is empty';
           }
         }
         else {
           alert('oblom');
         }
     })
     .always(function(){
       document.querySelector('.spinner-border').classList.add('d-none');
       document.querySelector('main').setAttribute( 'style',  'position: fixed; opacity:100% !important');
     })
  })
}

function add_deletion(){
  document.querySelectorAll('.delete_item').forEach(function(btn_del){
    deletion(btn_del);
  });
}


function add_menu(){
  document.querySelectorAll('.btn_add').forEach(btn_add => {
    btn_add.onclick = () => {
      var item_pk = btn_add.dataset.item_pk;
      var size = btn_add.dataset.item_size;
      var item_price = btn_add.dataset.item_price;
      var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
      $.post(url_add_to_cart, {
        item_pk: item_pk,
        size: size,
        price : item_price,
        user_id: user_id,
        csrfmiddlewaretoken: csrftoken }, function(){
          document.querySelector('.spinner-border').classList.remove('d-none');
          document.querySelector('main').setAttribute( 'style', 'position: fixed; opacity:50% !important');
        })
        .done(function( data ) {

          // все получилось
          if (data['status'] == "OK"){
            var cart = document.getElementById('order_t');
            var item_tr = document.createElement("tr");
            item_tr.classList.add("item_block")
            item_tr.id = "item-" + data['result'].item_id

            var item_td_del = document.createElement("td");
            var btn = document.createElement("button");
            btn.classList.add("close", "delete_item");
            btn.dataset.item_id = data['result'].item_id;
            btn.dataset.order_id = data['result'].order_id;
            btn.dataset.user_id = user_id;

            btn.onclick = deletion(btn);
            var btn_span = document.createElement("span");
            btn_span.title = "Delete an item";
            btn_span.innerHTML = "&times;";
            btn.appendChild(btn_span);
            item_td_del.appendChild(btn);

            var item_td = document.createElement("td");
            if (data['result'].type == 'Pasta' || data['result'].type ==  'Salads'){
              var txt = data['result'].type + '"' + data['result'].name + '"';
            }
            else if (data['result'].type == 'Sicilian Pizza' || data['result'].type ==  'Regular Pizza'){
              var txt = data['result'].size[0].toUpperCase() + data['result'].size.slice(1)+ ' "' + data['result'].type+ '" '+ data['result'].name;
            }
            else {
              var txt = data['result'].size[0].toUpperCase() + data['result'].size.slice(1)+ ' "' + data['result'].type+ '"';
            }
            var new_item = document.createTextNode( txt );
            item_td.appendChild(new_item);

            var brr = document.createElement("br");
            var topings_selector = document.createElement("select");
            alert(data['toppings'].itemtype);
            //<select name="select" data-topping1>
            //  <option value="value1" disabled selected>Choose toppings</option>
            //  {% for top in pizza_topings %}
            //    <option value="{{ top.pk }}">{{ top.name}}</option>
            //  {% endfor%}
            //</select>
            //extratop

            var item_td_price = document.createElement("td");
            var price_text = document.createTextNode("$" + data['result'].price);
            item_td_price.appendChild(price_text);

            item_tr.appendChild(item_td_del);
            item_tr.appendChild(item_td);
            item_tr.appendChild(item_td_price);
            cart.appendChild(item_tr);
            document.getElementById('total').innerHTML = ' Total: $' + data['result'].total.toFixed(2);
          }
          else {
            alert('oblom');
          }

      })
      .always(function(){
        document.querySelector('.spinner-border').classList.add('d-none');
        document.querySelector('main').setAttribute( 'style',  'position: fixed; opacity:100% !important');
      })
    };
  });
}

var TMP_ID = function () {
  // Math.random should be unique because of its seeding algorithm.
  // Convert it to base 36 (numbers + letters), and grab the first 9 characters
  // after the decimal.
  return '_' + Math.random().toString(36).substr(2, 9);
};




function logout(){
  document.querySelector('#logout').addEventListener(
      'click', function(){
        if (localStorage.getItem('temp_id')){
          localStorage.removeItem('temp_id');
        }
      }, true
  );
}

function signup_click(){
  document.querySelector('#signup_btn').addEventListener(
      'click', function(evnt){
        evnt.preventDefault();
        $('#signup_modal').modal('show');
      }, false
  );
}

function signup_submit(){
  document.querySelector('#signup_form').addEventListener(
    'submit', function(evnt){
      $('#signup').modal('hide');
      document.forms["signup_form"].submit();
    }
  );
}

function show_popover(){
  $('#user_account').popover('show');
}
function hide_popover(){
  $('#user_account').popover('hide');
}

function account_popover(){
var ul = document.getElementById("user_block");
  ul.addEventListener("mouseover", function(e) {
    if (e.target && (e.target.matches("#user_account") ||  e.target.matches("#user_account a") || e.target.matches(".gear"))) {
      setTimeout(show_popover, 300);
    }
  });

  ul.addEventListener("mouseout", function(e) {
    if (e.target && (e.target.matches("#user_account") || e.target.matches("#user_account a") || e.target.matches(".gear"))) {
      setTimeout(hide_popover, 300);
    }
  });
}


window.addEventListener('resize', window_resize);

function window_resize(){

var h = window.innerHeight - document.getElementById('foo').clientHeight - document.getElementById('nav').clientHeight - document.getElementById('extra_nav').clientHeight  + 'px';
$('#scrl').css('height', h);
$('#order_list').css('height', h, 'important');
}
