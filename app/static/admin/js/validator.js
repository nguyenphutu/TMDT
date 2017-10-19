var emailValidator =  {
    validator: function (value, element) {
        return this.optional(element) || /^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,10}|[0-9]{1,3})(\]?)$/.test(value);
    },
    message: "Please enter a valid email address.",
};

//My validation for check confirm password
$.validator.addMethod("confirmPassword", function (value, element, passwordName) {
    return value === $('input[name=' + passwordName + ']').val();
}, "Your password and confirmation password do not match.");

$.validator.addMethod("email2", emailValidator.validator, emailValidator.message);

function handleError(errorMap, errorList, errorElement) {
    if (errorList.length > 0) {
//
         $.each( errorMap, function( key, value ) {
            const label = $('span[name=' + key + ']');
            var message = value.replace('This field', label.html());

            message = message.replace('Field', label.html().toLowerCase());
            if ($('.error-message').length != 0){
                $('.error-message').remove()
            }
            label.after('<div class="error-message"><span class="text-danger ' + key + '-error">' + message + '</span></div>');
            return false;
        });

         return;
//
    }
    errorElement.html('');
}