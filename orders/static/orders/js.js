document.addEventListener('DOMContentLoaded', function(){
  add_deletion();
  add_menu();
  add_info();
  add_toppings_change();
  if (document.getElementById('checkout')){
    document.getElementById('checkout').addEventListener('click', function(){
      if (document.getElementById('checkout').dataset.order_id !=''){
        window.location.href = "/cabinet";
      }
      else{
        $("#pizza_info_modal").modal("show");
        $("#pizza_info_modal").find('#pizza_info_text').text('Please, choose something to make an order');
      }
    })
  }

  if (document.getElementById('make_order')){
    document.getElementById('make_order').addEventListener('click', function(){
      var check = true;
      document.querySelectorAll("select[data-type='Regular Pizza'], select[data-type='Sicilian Pizza']").forEach((select) => {
        if (select.value == 'null'){
          check = false;
        }
      });
      if (check){
        window.location.href = "/order_placing";
      }
      else{
        $("#pizza_info_modal").modal("show");
        $("#pizza_info_modal").find('#pizza_info_text').text('Please, select all toppings for pizza');
      }
    })
  }

if (document.getElementById('nav') && document.getElementById('extra_nav')) {
  var hh = window.innerHeight - document.getElementById('foo').clientHeight - document.getElementById('nav').clientHeight - document.getElementById('extra_nav').clientHeight  + 'px';
 $('#scrl').css('height', hh);
 $('#order_list').css('height', hh, 'important');
}

if (document.querySelector('#signup_btn')){
    signup_click();
    signup_submit();
  }
if (document.querySelector('#user_account')){
    logout();
    account_popover();
  }
});

function add_toppings_change(){
    document.querySelectorAll('.topings').forEach(function(top_elm){
      toppings(top_elm);
    });
}


function disable_doubles(item, selector){
  var selectors = item.getElementsByClassName("topings")
  for (var z = 0; z < selectors.length; z++ ) {
    if (z != selector && selectors[selector] && selectors[selector].value != 'null'){
      selectors[z].options[selectors[selector].dataset.previos].disabled = false
      selectors[z].options[selectors[selector].selectedIndex].disabled = true;
    }
    if (selectors[selector]){
      selectors[selector].dataset.previos = selectors[selector].selectedIndex;
    }
  }
  if (selector < selectors.length){
    disable_doubles(item, selector+1);
  }
}

function toppings(elm){
  elm.addEventListener("change", function(){
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    var topings_lists = elm.parentElement.getElementsByClassName("topings")
    var toppings_array = {};
    for (var i = 0; i < topings_lists.length; i++) {
      toppings_array[i] = topings_lists[i].value;
    }

    $.post(add_topings, {
        'order_item_pk':  elm.parentElement.dataset.order_item,
        'csrfmiddlewaretoken': csrftoken,
        'topping_pk_array': JSON.stringify(toppings_array)
    } ,
      function(){
        document.querySelector('.spinner-border').classList.remove('d-none');
        document.querySelector('main').setAttribute( 'style', 'position: fixed; opacity:50% !important');
      })
      .done(function( data ) {

        // все получилось
        if (data['status'] == "OK"){
          document.getElementById('price'+data['item_pk']).innerHTML = '$' + parseFloat(data['total_item']).toFixed(2);
          document.getElementById('total').innerHTML = ' Total: $' + parseFloat(data['total_order']).toFixed(2);
          for (let topings_list of topings_lists) {
            if (topings_list != elm){
              topings_list.options[elm.dataset.previos].disabled = false
              if (elm.value != "null"){
                topings_list.options[elm.selectedIndex].disabled = true;
              }
            }
          }
            elm.dataset.previos = elm.selectedIndex;
        }
        else {
          alert(data['status']);
        }
    })
    .always(function(){
      document.querySelector('.spinner-border').classList.add('d-none');
      document.querySelector('main').setAttribute( 'style',  'position: fixed; opacity:100% !important');
    })
  })
}

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
             //блокируем кнопку размещения заказа
             document.getElementById('checkout').dataset.order_id = '';
           }
         }
         else {
           alert(data['status']);
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

function add_info(){
  document.querySelectorAll('.btn_info').forEach(btn_info => {
    btn_info.onclick = () => {
      $("#pizza_info_modal").modal("show");
      $("#pizza_info_modal").find('#pizza_info_text').text(btn_info.dataset.item_info);
    }
  })
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
            //разблокируем кнопку заказа
            document.getElementById('checkout').dataset.order_id = data['result'].order_id;
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
            item_td.dataset.order_item = data['result'].item_id;
            if (data['result'].type == 'Pasta' || data['result'].type ==  'Salads'){
              var txt = data['result'].type + '"' + data['result'].name + '"';
            }
            else if (data['result'].type == 'Sicilian Pizza' || data['result'].type ==  'Regular Pizza'){
              var txt = data['result'].size[0].toUpperCase() + data['result'].size.slice(1)+ ' "' + data['result'].type+ '" '+ data['result'].name;
            }
            else {
              var txt = data['result'].size[0].toUpperCase() + data['result'].size.slice(1)+ ' ' + data['result'].type + ' "' + data['result'].name+ '"';
            }
            var new_item = document.createTextNode( txt );
            item_td.appendChild(new_item);
            // добавляем столько дропдаунов, сколько позволяет item
            var top = data['result'].extratop;
            while (top > 0) {
              var brr = document.createElement("br");
              item_td.appendChild(brr);
              var topings_selector = document.createElement("select");
              topings_selector.classList.add("topings");
              topings_selector.dataset.previos = 0;

              var def = document.createElement("option");
              if (data['result'].type != 'Subs'){
                def.disabled = "disabled";
              }
              def.selected = "selected";
              def.innerHTML = "Choose toppings";
              def.value = "null";
              topings_selector.appendChild(def);

              for (var i = 0; i < data['toppings'].length; i++){
                var itm = document.createElement("option");
                itm.value = data['toppings'][i]['pk'];
                var price_and_name = data['toppings'][i]['name'];
                  if (data['toppings'][i]['price'] != 0){
                      price_and_name += ' + $'+data['toppings'][i]['price'];
                  }
                itm.innerHTML = price_and_name;
                topings_selector.appendChild(itm);
              }
              item_td.appendChild(topings_selector);
              topings_selector.onchange = toppings(topings_selector);
              top -= 1;
            }

            var item_td_price = document.createElement("td");
            item_td_price.id= 'price' + data['result'].item_id;
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
  if (document.getElementById('extra_nav') && document.getElementById('nav')){
    var h = window.innerHeight - document.getElementById('foo').clientHeight - document.getElementById('nav').clientHeight - document.getElementById('extra_nav').clientHeight  + 'px';
    $('#scrl').css('height', h);
    $('#order_list').css('height', h, 'important');
  }
}
