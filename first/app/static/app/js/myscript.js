$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


//increase the items in the cart

$('.positive').click(function(){
    var id=$(this).attr("pid").toString();
    var elm=this.parentNode.children[2]
    $.ajax({
    type:"GET",
    url:"/pluscart",
    data:{
    prod_id:id
    },
    success:function(data) {
    elm.innerText=data.quantity
    document.getElementById("amount").innerText=data.amount
    document.getElementById("totalamount").innerText=data.totalamount

    }
    })
})

//decrease the items in the cart

$('.negative').click(function(){
    var id=$(this).attr("pid").toString();
    var elm=this.parentNode.children[2]
    $.ajax({
    type:"GET",
    url:"/minuscart",
    data:{
    prod_id:id
    },
    success:function(data) {
    elm.innerText=data.quantity
    document.getElementById("amount").innerText=data.amount
    document.getElementById("totalamount").innerText=data.totalamount

    }
    })
})

//for remove items in the cart

$('.remove').click(function(){
    var id = $(this).attr("pid").toString();
    var elm = this;
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;

            if (data.empty_cart) {
                // Handle empty cart UI updates
                $('#cart-items').html('<p>Your cart is empty.</p>');
            } else {
                // Update or remove the item element
                var itemQuantity = $(elm).closest('.cart-item').find('.item-quantity');
                if (itemQuantity.text() > 1) {
                    itemQuantity.text(itemQuantity.text() - 1);
                } else {
                    elm.parentNode.parentNode.parentNode.parentNode.parentNode.remove();
                }
            }
        }
    });
});

