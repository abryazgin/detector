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
    var url = ""
    $('#myFormResults').submit(function (e) {
        e.preventDefault();
        var data = new FormData($('#myFormLoad').get(0));
        $('#app_photo_s').css('visibility', 'visible');
        var myNode = document.getElementById("results");
        while (myNode.firstChild) {
            myNode.removeChild(myNode.firstChild);
        }
        console.log($('app_photo_s'))
        data.append("url", url)
        $.ajax({
            cache: true,
            dataType: 'json',
            processData: false,
            contentType: false,
            // get the form data
            data: data,
            csrfmiddlewaretoken: '{{ csrf_token }}',
            // GET or POST
            type: $('#myFormResults').attr('method'),
            // the file to call
            url: $('#myFormResults').attr('action'),

            success: function (response) {
                //$('#app_photo_s').css('visibility', 'hidden');
                if (response['result'] == 'success') {
                    console.log('SUCCESS', response)
                    var myNode = document.getElementById("results");
                    while (myNode.firstChild) {
                        myNode.removeChild(myNode.firstChild);
                    }
                    for (var p in response['response']) {
                        var path = response['response'][p]['imgPath']
                        var newdiv = document.createElement('div');
                        var elem = document.createElement("img");
                        elem.setAttribute("src", path);
                        newdiv.appendChild(elem);

                        myNode.appendChild(newdiv);
                    }


                }
                else if (response['result'] == 'error') {
                    console.log('OK error', response);
                    bootstrap_alert(response['response'])
                }
            },
            error: function (response) {
                $('#app_photo_s').css('visibility', 'hidden');
                // Displays the error message.
                console.log('error', response.responseText)
                bootstrap_alert("Ошибка при загрузке")
            },
        });
    })

    var get_results = function (url1) {
        url = url1;
        console.log(url1)
        $('#myFormResults').submit()
    }

    if ($('#current_photo').length > 0) {
        get_results($('#current_photo').attr('src'))
    }

    $('#myFormLoad').submit(function (e) {
        e.preventDefault();
        // create an AJAX call…
        var data = new FormData($('#myFormLoad').get(0));
        console.log('AJAX!!!', $('#myFormLoad').attr('method'), $('#myFormLoad').attr('action'), data)

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
            type: $('#myFormLoad').attr('method'),
            // the file to call
            url: $('#myFormLoad').attr('action'),
            // on success..

            success: function (response) {
                if (response['result'] == 'success') {
                    console.log('SUCCESS', response)
                    $('#current_photo').attr('src', response["url"])

                    get_results(response['url'])
                }
                else if (response['result'] == 'error') {
                    console.log('OK error', response);
                    bootstrap_alert(response['response'])
                }
            },
            error: function (response) {
                // Displays the error message.
                console.log('error', response.responseText)
                bootstrap_alert("Ошибка при загрузке")
            },
        });
    });
    $('#photo').on('change', function (e) {
        console.log('CHANGE')
        $('#myFormLoad').submit();
    });
    $('#start_load').on('click', function (e) {
        console.log('CLICK')
        $('#photo').click()
    });

});
