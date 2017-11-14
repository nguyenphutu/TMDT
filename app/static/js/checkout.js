var CheckoutForm = $('#checkout-form');
var errorMessage = $('.error-message');

if(CheckoutForm.length) {
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
            'fullname': {
                required: true,
                minlength: 4,
                maxlength: 255,
            },
            'city': {
                required: true,
                minlength: 2,
                maxlength: 255,
            },
            'district': {
                required: true,
                minlength: 2,
                maxlength: 255,
            },
            'ward': {
                required: true,
                minlength: 2,
                maxlength: 255,
            },
            'address': {
                required: true,
                minlength: 2,
                maxlength: 255,
            },
            'phone': {
                required: true,
                minlength: 9,
                maxlength: 12,
            },

        },
    };
    // add email pattern
//    $.validator.addMethod("email2", email.validator, email.message);
    validator = CheckoutForm.validate(options);

//    btnSubmit.click(function () {
//        CheckoutForm.submit();
//    });
}

