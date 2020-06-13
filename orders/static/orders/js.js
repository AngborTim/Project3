var TMP_ID = function () {
  // Math.random should be unique because of its seeding algorithm.
  // Convert it to base 36 (numbers + letters), and grab the first 9 characters
  // after the decimal.
  return '_' + Math.random().toString(36).substr(2, 9);
};

document.addEventListener('DOMContentLoaded', function(){
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
