var activateLoadFileOnce = function () {
    $('#start_load').one('click', choose_file);
}

var activateRestart = function () {
    $('#restart_load').click(function () {
        $('#load_section').css('display', 'block');
        $('#result_section').css('display', 'none');
    })
}

var activateClickSearchLogo = function () {
    $('.search_logo_link').click(function () {
        var $button_just_clicked_on = $(this);
        var stat_id = $button_just_clicked_on.data('stat_id');
        console.log('qwe', stat_id)
        save_stat(stat_id);
    })
}

var search_logo_callback = function (response) {
    console.log('search_logo_callback')
    $('#spinner_search').css('visibility', 'hidden');
    $('#finded_logo').html(response)
    activateLoadFileOnce();
    activateClickSearchLogo();
}

var search_logo_errback = function (response) {
    console.log('error', response.responseText)
    $('#spinner_search').css('visibility', 'hidden');
    activateLoadFileOnce();
    bootstrap_alert("Ошибка при загрузке")
}

var check_image_callback = function (response) {
    $('#spinner_load').css('visibility', 'hidden');
    if (response['result'] == 'success') {
        console.log('SUCCESS', response)
        //$("#file_output").attr("src", URL.createObjectURL(event.target.files[0]));
        $('#load_section').css('display', 'none');
        $('#result_section').css('display', 'block');
        $('#file_output').attr('src', response["img"])
        $('#spinner_search').css('visibility', 'visible');
        $('#finded_logo').html("")
        search_logo(search_logo_callback, search_logo_errback);
    }
    else if (response['result'] == 'error') {
        console.log('OK error', response);
        activateLoadFileOnce();
        bootstrap_alert(response['data'])
    }
}

var check_image_errback = function (response) {
    console.log('error', response.responseText)
    $('#spinner_load').css('visibility', 'hidden');
    activateLoadFileOnce();
    bootstrap_alert("Ошибка при загрузке")
}

var manage_file = function (event) {
    $('#spinner_load').css('visibility', 'visible');
    //$('#current_photo').attr('src', "")
    check_image(check_image_callback, check_image_errback)
}

var save_stat = function(stat_id)  {

    var callback = function(data)  {
        console.log('save_stat', data)
    }

    var config = {
        url: 'save_stat',
        type: 'GET',
        data: {stat_id: stat_id},
        success: callback,
        error: callback
    };
    $.ajax(config)
};

$(document).ready(function () {
    downloadPrevPhoto();

    set_action_on_choose_file(manage_file);
    //window.location.href = SEARCH_URL + "/" + data.pk;
    activateLoadFileOnce();
    activateRestart();
})