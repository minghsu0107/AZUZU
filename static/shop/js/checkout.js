if (localStorage.getItem('cart') == null) {
    var cart = {};
} 
else {
    cart = JSON.parse(localStorage.getItem('cart'));
}

let total = 0;

//console.log(cart);

for (item in cart) {
    let name = cart[item][1];
    let quantity = cart[item][0];
    let price = cart[item][2];
    let sum = parseFloat(price) * Number(quantity);
    total += sum;
    price = numberWithCommas(price);
    sum = numberWithCommas(sum);

    itemString = `<div class="col-xs-12"><li class="list-group-item d-flex justify-content-between align-items-center">
        <div class="col-xs-8">${name}</div>
        <span class="col-xs-4 badge badge-warning badge-pill">${price} x ${quantity} = ${sum}</span></li></div>`;

    $('#item_list').append(itemString);

}
let sum = numberWithCommas(total);
totalPrice = `<li class ="list-group-item d-flex justify-content-between align-items-center">
    <div class="col-xs-3"><b>Total</b></div>${sum}</li>`
$('#item_list').append(totalPrice);

total = numberWithCommas(total + Number(document.getElementById("shipping").value));
$('#total').val(total);
$('#items').val(JSON.stringify(cart));

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}