$(document).ready(function () {

     $( "#change-product-img" ).click(function() {
      $( ".input-img-file" ).click();
    });

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#product-image').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $(".input-img-file").change(function(){
        readURL(this);
    });

});
