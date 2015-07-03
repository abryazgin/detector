$(document).ready(function () {
    // catch the submit event of the form.
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

    $('#myFormLoad').submit(function (e) {
        e.preventDefault();
        // create an AJAX call…
        var data = new FormData($('#myForm').get(0));
        console.log('AJAX!!!', $('#myForm').attr('method'), $('#myForm').attr('action'), data)

        $.ajax({
            cache: true,
            dataType: 'json',
            processData: false,
            contentType: false,
            xhr: function () {

                var xhr = new window.XMLHttpRequest();
                var in_progress = false;
                //Upload progress
                xhr.upload.addEventListener("progress", function (e) {
                    if (e.lengthComputable) {
                        var percentComplete = e.loaded / e.total;
                        console.log('percent', percentComplete)
                        if (percentComplete > 0 && percentComplete <= 1) {
                            if (!in_progress) {
                                in_progress = true;
                                $('#spinner_load').css('visibility', 'visible');
                            }
                            if (percentComplete == 1) {
                                in_progress = false
                                $('#spinner_load').css('visibility', 'hidden');
                                //setTimeout(
                                //    function () {
                                //        $('#spinner_load').css('visibility', 'hidden');
                                //    }, 1000)


                            }

                        }


                    }
                }, false);
                return xhr;
            },

            // get the form data
            data: data,
            csrfmiddlewaretoken: '{{ csrf_token }}',
            // GET or POST
            type: $('#myForm').attr('method'),
            // the file to call
            url: $('#myForm').attr('action'),
            // on success..
            success: function (response) {
                // Displays the success message.
                console.log('success', response)

            },
            success: function(response) {
                if (response['result'] == 'success') {
                    console.log('SUCCESS', response)
                }
                else if (response['result'] == 'error') {
                    console.log('OK error', response);
                    bootstrap_alert(response['response'])
                }
            },
            error: function (response) {
                // Displays the error message.
                console.log('error', response)
                bootstrap_alert("Ошибка при загрузке")
            },
        });
    });
    $('#photo').on('change', function (e) {
        console.log('CHANGE')
        $('#myForm').submit();
    });
    $('#start_load').on('click', function (e) {
        console.log('CLICK')
        $('#photo').click()
    });


});
