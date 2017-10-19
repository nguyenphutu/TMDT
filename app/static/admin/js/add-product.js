var AddProductForm = $('#add-product-form');
var errorMessage = $('.error-message');

if(AddProductForm.length) {
    btnSubmit = $('#btn-submit'),
    validator = {};
    options = {

        errorElement: "span",
        errorClass: "text-danger",

//        errorPlacement: function(error) {
//            errorMessage.html(error);
//        },

        success: function () {
        },

        rules: {
            'name': {
                required: true,
                minlength: 1,
                maxlength: 255,
            },
            'quantity': {
                required: true,
                minlength: 1,
                maxlength: 10,
            },
            'price': {
                required: true,
                minlength: 1,
                maxlength: 10,
            },
            'category': {
                required: true,
                minlength: 1,
                maxlength: 10,
            },

        },
    };
    // add email pattern
//    $.validator.addMethod("email2", email.validator, email.message);
    validator = AddProductForm.validate(options);

    btnSubmit.click(function () {
        AddProductForm.submit();
    });
}

