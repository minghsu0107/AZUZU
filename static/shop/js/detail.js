let add_form = document.getElementById('view-add'),
    add_input = document.getElementById('view-add-input');
add_form.addEventListener('submit', addCart);

function addCart(e) {
    e.preventDefault();
    [cart, num_items] = fetch();
    num_items = Number(num_items);

    item_key = e.target[0].id;
    value = Number(add_input.value);

    if (item_key in cart) {
        original_quantity = Number(cart[item_key][0]);
        cart[item_key][0] = original_quantity + value;
    }
    else {
        name = document.getElementById("nm"+item_key).innerHTML;
        price = parseFloat(document.getElementById("price"+item_key).innerHTML.replace(',',''));
        cart[item_key] = [value, name, price];
    }
    num_items += value;
    add_form.reset();
    saveToLocalStorage(cart, num_items);

    DisplayCart(cart);
    $('[data-toggle="popover"]').popover();
}

function fetch() {
    if (localStorage.getItem('cart')==null){
        var cart = {};
        var num_items = 0;
    }
    else{
        cart = JSON.parse(localStorage.getItem('cart'));
        num_items = localStorage.getItem('num_items')
    }
    return [cart, num_items];
}

function DisplayCart(cart){
    var cartString ="<div class='cur-cart' style='max-height: 500px;'>";
    cartString += "<center><h5>Your Cart</h5></center>";
    if (Object.keys(cart).length != 0) {
        cartString += `<div class='trash-alignment'><button onclick="removeAll()" class='btn btn-outline-danger' id='clean'><i class="fa fa-trash"></i></button></divbr></div>`;
    }
    else {
        cartString += '<img src="/static/shop/img/empty-cart.jpg" width="250" height="120" style="margin-left: 18%">';
    }
    for(var item_key in cart){
        var quantity = '<input onclick="modifyItem(this.id, this.value)" type="number" id="'+ 'quan' + item_key + '" class="form-control input-number" value="'+cart[item_key][0]+'" min="1">'
        var delete_button = '<div class="input-group-prepend"><span class="input-group-btn"><a onclick="removeItem(this.id)" id="' + 'del_b' + item_key + '" class="btn btn-danger btn-sm float-right x-button">x</a></span></div>';
        cartString += '<div class="col-md-12 cur-cart-item">' + cart[item_key][1]  + '</div>' + '<div class="col-md-12"><form onsubmit=" return modifyItemOnSubmit(this);"><div class="input-group">' + delete_button + quantity + '</div></form></div>';
    }
    $('[data-toggle="popover"]').popover('dispose');
    cartString += "<center><a href='/checkout'><button class='btn btn-warning' id='checkout'>Checkout</button></a></center>";
    cartString += "</div>";
    document.getElementById("cart").setAttribute('data-content',cartString);
}

function modifyItemOnSubmit(form) {
    [cart, num_items] = fetch();
    num_items = Number(num_items);

    key = form.elements[0].id;
    value = form.elements[0].value;

    var item_key = key.substring('quan'.length, key.length);

    original_quantity = Number(cart[item_key][0]);
    new_quantity = Number(value);
    diff = new_quantity - original_quantity;
    cart[item_key][0] = new_quantity;

    num_items += diff;
    saveToLocalStorage(cart, num_items);
    return false;
}

function modifyItem(key, value) {
    [cart, num_items] = fetch();
    num_items = Number(num_items);
    
    var item_key = key.substring('quan'.length, key.length);

    original_quantity = Number(cart[item_key][0]);
    new_quantity = Number(value);
    diff = new_quantity - original_quantity;
    cart[item_key][0] = new_quantity;

    num_items += diff;
    saveToLocalStorage(cart, num_items);
}

function removeItem(key) {
    [cart, num_items] = fetch();

    var item_key = key.substring('del_b'.length, key.length);
    
    original_quantity = Number(cart[item_key][0]);
    
    delete cart[item_key];

    num_items -= original_quantity;
    saveToLocalStorage(cart, num_items);

    DisplayCart(cart);
    $('[data-toggle="popover"]').popover('show');
    alert('yyyy');
}

function removeAll() {
    localStorage.removeItem('cart');
    localStorage.removeItem('num_items');

    cart = {};
    DisplayCart(cart);
    $('[data-toggle="popover"]').popover('show');

    document.getElementById("cart").innerHTML = "<i class='fa fa-shopping-cart'></i>(0)";
}

function saveToLocalStorage(cart, num_items) {
    localStorage.setItem('cart',JSON.stringify(cart));
    localStorage.setItem('num_items',num_items);
    document.getElementById("cart").innerHTML = "<i class='fa fa-shopping-cart'></i>("+ num_items +")";
}