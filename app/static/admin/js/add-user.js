var AddUserForm = $('#add-user-form');
var errorMessage = $('.error-message');

if(AddUserForm.length) {
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
            'first_name': {
                required: true,
                minlength: 1,
                maxlength: 255,
            },
            'last_name': {
                required: true,
                minlength: 1,
                maxlength: 255,
            },
            'email': {
                required: true,
                email2: true,
                minlength: 1,
                maxlength: 255,
            },
            'password': {
                required: true,
                minlength: 6,
                maxlength: 50,
            },
            'role': {
                required: true,
                minlength: 1,
                maxlength: 50,
            },

        },
        messages: {
            'first_name': {
                required: "First name is required",
                minlength: jQuery.validator.format("At least {0} characters required!"),
                maxlength: jQuery.validator.format("At most {0} characters required!"),
            },
            'last_name':{
                required: "Last name is required",
                minlength: jQuery.validator.format("At least {0} characters required!"),
                maxlength: jQuery.validator.format("At most {0} characters required!"),
            },
            'email':{
                required: "Email code is required",
                email2: "Please enter a valid email address.",
                minlength: jQuery.validator.format("At least {0} characters required!"),
                maxlength: jQuery.validator.format("At most {0} characters required!"),
            },
            'password':{
                required: "Password is required",
                minlength: jQuery.validator.format("At least {0} characters required!"),
                maxlength: jQuery.validator.format("At most {0} characters required!"),
            },
            'role':{
                required: "Role is required",
                minlength: jQuery.validator.format("At least {0} characters required!"),
                maxlength: jQuery.validator.format("At most {0} characters required!"),
            },
        }
    };
    // add email pattern
//    $.validator.addMethod("email2", email.validator, email.message);
    validator = AddUserForm.validate(options);

    btnSubmit.click(function () {
        AddUserForm.submit();
    });
}

