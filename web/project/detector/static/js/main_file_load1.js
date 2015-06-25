$(document).ready(function () {
    // catch the submit event of the form.
    $('#myForm').submit(function (e) {
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
                //Upload progress
                xhr.upload.addEventListener("progress", function (e) {
                    if (e.lengthComputable) {
                        $('.progress').css('visibility', 'visible');
                        var percentComplete = e.loaded / e.total;
                        //Do something with upload progress
                        console.log('percent', percentComplete)
                        $('.progress-bar').css('width', (percentComplete) * 100 + '%');
                        if (percentComplete == 1){
                            $('.progress').css('visibility', 'hidden');
                            $('.progress-bar').css('width', '0%');
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
            error: function (response) {
                // Displays the error message.
                console.log('error', response)
            },
        });
    });
    $('#photo').on('change',function (e) {
        console.log('CHANGE')
        $('#myForm').submit();
    });
    $('#start_load').on('click', function (e) {
        console.log('CLICK')
        $('#photo').click()
    });



});
