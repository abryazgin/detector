var form_ajax = function (action, dataType, callback, errback) {
    var data = new FormData($('#loadFileForm').get(0));
    config = {
        cache: true,
        dataType: dataType,
        processData: false,
        contentType: false,
        data: data,
        csrfmiddlewaretoken: '{{ csrf_token }}',
        type: 'POST',
        // the file to call
        url: action,
        success: function (response) {
            response['img'] = URL.createObjectURL($('#file_id')[0].files[0]);
            if (callback) {
                callback(response)
            }
        },
        error: function (response) {
            if (errback) {
                errback(response)
            }
        },
    };
    console.log(config);
    $.ajax(config);
}

var search_logo = function (callback, errback) {
    $('#loadFileForm').submit(function (e) {
        e.preventDefault();
        form_ajax('search_logo', 'html',  callback, errback);
    })
    $('#loadFileForm').submit();
}

var check_image = function (callback, errback) {
    form_ajax('check_image', 'json', callback, errback);
}

var set_action_on_choose_file = function (calback) {
    $('#file_id').on('change', function (e) {
        console.log('CHANGE');
        if (calback) {
            calback(e)
        }
    });
}

var choose_file = function () {
    $('#file_id').click()
}

var initLoad = function (previewFile, callback_func, spinnerId) {

    //$('#loadFileForm').submit(function (e) {
    //    e.preventDefault();
    //    $('#' + spinnerId).css('visibility', 'visible');
    //    // create an AJAX call…
    //    var data = new FormData($('#loadFileForm').get(0));
    //    console.log('AJAX!!!', $('#loadFileForm').attr('method'), $('#loadFileForm').attr('action'), data)
    //
    //    $.ajax({
    //        cache: true,
    //        dataType: 'json',
    //        processData: false,
    //        contentType: false,
    //
    //        // get the form data
    //        data: data,
    //        csrfmiddlewaretoken: '{{ csrf_token }}',
    //        // GET or POST
    //        type: $('#loadFileForm').attr('method'),
    //        // the file to call
    //        url: $('#loadFileForm').attr('action'),
    //        // on success..
    //
    //        success: function (response) {
    //            $('#' + spinnerId).css('visibility', 'hidden');
    //            if (response['result'] == 'success') {
    //                console.log('SUCCESS', response)
    //
    //                if (callback_func){
    //                    callback_func(response["data"]);
    //                }
    //            }
    //            else if (response['result'] == 'error') {
    //                console.log('OK error', response);
    //                bootstrap_alert(response['data'])
    //            }
    //        },
    //        error: function (response) {
    //            $('#' + spinnerId).css('visibility', 'hidden');
    //            // Displays the error message.
    //            console.log('error', response.responseText)
    //            bootstrap_alert("Ошибка при загрузке")
    //        },
    //    });
    //});
}

