$('.value-plus').on('click', function(){
    var id = $(this).data('id');
    var quantity = $('#quantity-'+id).text()
    var divPrice = $('#price-'+id)
    var divUpd = $(this).parent().find('.value'), newVal = parseInt(divUpd.text(), 10)+1;
    var Price = parseFloat(divPrice.text())/parseFloat(divUpd.text())
    divUpd.text(newVal);
    newPrice = (Price*newVal).toFixed(2);
    divPrice.text(newPrice);
    var save_change = $('#change-'+id);
    $('#delete-'+id).css({ 'display': "none" });
    save_change.css({ 'display': "block" });
    save_change.attr('data-value', newVal);

});

$('.value-minus').on('click', function(){
    var id = $(this).data('id');
    var quantity = $('#quantity-'+id).text()
    var divPrice = $('#price-'+id)
    var divUpd = $(this).parent().find('.value'), newVal = parseInt(divUpd.text(), 10)-1;
    var Price = parseFloat(divPrice.text())/parseFloat(divUpd.text())
    if(newVal>=1) divUpd.text(newVal);
    newPrice = (Price*newVal).toFixed(2);
    if(newVal>=1)divPrice.text(newPrice);
    var save_change = $('#change-'+id);
    $('#delete-'+id).css({ 'display': "none" });
    save_change.css({ 'display': "block" });
    save_change.attr('data-value', newVal);
});

$('.btn-delete-order').click(function(){
    $('#delete-user-form').attr('action', $(this).data('id'));
});
$('.save-change').click(function(){
    var form = $('#update-product');
    form.attr('action', $(this).data('id'));
    $("input[name='quality']").val($(this).data('value'));
});