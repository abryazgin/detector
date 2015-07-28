var bootstrap_alert = function (message) {
    if ($('#alertdiv').length > 0) {
        $('#alertdiv').alert('close')
    }

    $('#alert_placeholder').html('<div id="alertdiv" class="alert alert-danger alert-dismissible">' +
        '<a class="close" data-dismiss="alert">×</a>' +
        '<span>' + message + '</span>' +
        '</div>')

    setTimeout(function () {
        //this will automatically close the alert and remove this if the users doesnt close it in 5 secs
        if ($('#alertdiv').length > 0) {
            $('#alertdiv').alert('close')
        }

    }, 5000);
}