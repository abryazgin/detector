var save = function () {
    $('#saveForm').submit();
}

var activateClickSaveOnce = function () {
    $('#buttonSave').one('click', save);

    document.getElementById('button_save').disabled = false;
    $('#spinner_load').css('visibility', 'hidden');
}

var activateFormAction = function () {
    $('#saveForm').submit(function (e) {
        $('#spinner_load').css('visibility', 'visible');
        document.getElementById('button_save').disabled = true;

        console.log($('#spinner_load'))
        e.preventDefault();
        var data = new FormData($('#saveForm').get(0));
        config = {
            cache: true,
            dataType: 'json',
            processData: false,
            contentType: false,
            data: data,
            csrfmiddlewaretoken: '{{ csrf_token }}',
            type: 'POST',
            // the file to call
            url: $('#saveForm').attr('action'),
            success: function (response) {
                console.log('OK ', response);

                if (response['result'] == 'success') {
                    var next = response['next'];
                    if (next) {
                        window.location.href =next;
                    } else {
                        bootstrap_alert('Не пришла ссылка для перехода дальше.')
                    }
                }
                else if (response['result'] == 'error') {
                    bootstrap_alert(response['data'])
                }
                activateClickSaveOnce();
            },
            error: function (response) {
                console.log('error', response)
                activateClickSaveOnce();

                bootstrap_alert('Ошибка при сохранении')
            },
        };
        $.ajax(config);
    })
}

$(document).ready(function () {
    activateFormAction();
    activateClickSaveOnce();
})