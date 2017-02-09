function setPrice() {
    var price = $(".variation_select option:selected").attr("data-price");

    var sale_price = $(".variation_select option:selected").attr("data-sale-price");
    if (sale_price != "" && sale_price != "None" && sale_price != null) {
        $("#price").html("<h3>" + sale_price + " <small class='original-price'>" + price + "</small></h3>");
    } else {
        $("#price").text(price);
    }

    var img = $(".variation_select optioin:selected").attr("data-img");
    $("img").attr("src", img);
}

function showFlashMessage(message){
    var template = "<div class='row'><div class='col-sm-3 col-sm-offset-8'><div class='container-alert-flash alert alert-success alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>" + message + "</div></div></div>"

    console.log(template);
    $(".alert-container").html(template);
    $(".container-alert-flash").fadeIn();
    setTimeout(function(){
        $(".container-alert-flash").fadeOut();
    }, 1000);   
}