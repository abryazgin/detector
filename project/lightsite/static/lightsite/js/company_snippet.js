var logoLoad = function () {
    var $button_just_clicked_on = $(this);
    var company_id = $button_just_clicked_on.data('company_id');
    //console.log('logoLoad', company_id, $button_just_clicked_on)
    $('#file_id' + company_id).click()
}

var activateAllLoadLogoOnce = function () {
    $('.load_logo_company').one('click', logoLoad);
}

var logoRemove = function () {
    var $button_just_clicked_on = $(this);
    var logo_id = $button_just_clicked_on.data('logo_id');
    //console.log('logoRemove', logo_id, $button_just_clicked_on.attributes)
    removeLogo(logo_id)
}

var activateAllRemoveLogoOnce = function () {
    $('.remove_logo_company').one('click', logoRemove);
}

var activateOneRemoveLogoOnce = function (logo_id) {
    $('#remove_logo_company' + logo_id).one('click', logoRemove);
}

var activateOneLoadLogoOnce = function (company_id) {
    $('#load_logo_company' + company_id).one('click', logoLoad);
}

var onChangeFile = function (event) {
    var $input_just_changed_on = $(event.currentTarget);
    var company_id = $input_just_changed_on.data('company_id');
    $('#spinner_load' + company_id).css('visibility', 'visible');

    saveLogo(company_id)
}

var setActionOnAllChooseLogo = function () {
    $('.file_logo').on('change', function (e) {
        onChangeFile(e)
    });
}

var form_ajax = function (data, action, dataType, callback, errback) {

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
    //console.log(config);
    $.ajax(config);
}

var saveLogo = function (company_id) {
    var form_id = '#loadLogoForm' + company_id;
    var data = new FormData($(form_id).get(0));

    var callback = function (response) {
        console.log('callback', company_id)
        $('#spinner_load' + company_id).css('visibility', 'hidden');
        $('#logos_' + company_id).append(response)
        var a_tag = $(response).children('a');
        var logo_id = a_tag.data('logo_id')
        //console.log(logo_id)
        activateOneLoadLogoOnce(company_id);
        activateOneRemoveLogoOnce(logo_id);
    }

    var errback = function (response) {
        console.log('error', company_id, response.responseText)
        $('#spinner_load' + company_id).css('visibility', 'hidden');
        activateOneLoadLogoOnce(company_id);
        bootstrap_alert("Ошибка при загрузке")
    }

    $(form_id).submit(function (e) {
        e.preventDefault();
        form_ajax(data, 'save_logo', 'html', callback, errback);
    })
    $(form_id).submit();
}

var removeLogo = function (logo_id) {
     var removeCallback = function(data)  {
        console.log('removeCallback', data)
        $('#logo_img_div' + logo_id).empty();
    }

    var removeErrback =  function(data)  {
        console.log('removeErrback', data.responseText)
        bootstrap_alert("Ошибка при удалении");
        activateOneRemoveLogoOnce(logo_id);
    }

    var config = {
        url: 'remove_logo',
        type: 'GET',
        data: {logo_id: logo_id},
        success: removeCallback,
        error: removeErrback
    };
    $.ajax(config);
}







