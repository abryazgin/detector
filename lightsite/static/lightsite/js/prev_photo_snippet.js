var downloadPrevPhoto = function()  {

    var setPrevPhoto = function(data, textStatus_ignored, jqXHR_ignored)  {
        //alert("sf data='" + data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "', color_id='" + color_id + "'");
        console.log('PREV PHOTO have got')
        $('#prev_photo').html(data);

    }

    var config = {
        url: 'get_prev_photo',
        dataType: 'html',
        success: setPrevPhoto
    };
    $.ajax(config);
};

