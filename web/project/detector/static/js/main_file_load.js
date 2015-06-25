// Generate 32 char random uuid
function gen_uid() {
    var uuid = ""
    for (var i = 0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
    }
    return uuid
}

$('#X-Progress-ID').val(gen_uid());

var options = {
    dataType: 'xml',
    url: '/upload?X-Progress-ID=' + $('#X-Progress-ID').val(),
    beforeSubmit: showRequest,
    success: showResponse
}
console.log($('#X-Progress-ID'), options)
$('#form_upload').ajaxSubmit(options);

function showRequest(formData, jqForm, options) {
    // do something with formData
    return true;
}

function showResponse(response) {
    // do something with response
}

$('#form_upload').find('#form_submit_input').append('&lt;span id="uploadprogressbar"&gt;&lt;/span&lt;');
$('#form_upload').find('#uploadprogressbar').progressBar();

function startProgressBarUpdate(upload_id) {
    console.log("startProgressBarUpdate")
    $("#uploadprogressbar").fadeIn();
    if (g_progress_intv != 0)
        clearInterval(g_progress_intv);
    g_progress_intv = setInterval(function () {
        $.getJSON("/lightsite/get_upload_progress?X-Progress-ID="
            + upload_id, function (data) {
            if (data == null) {
                $("#uploadprogressbar").progressBar(100);
                clearInterval(g_progress_intv);
                g_progress_intv = 0;
                return;
            }
            var percentage = Math.floor(100 * parseInt(data.uploaded) / parseInt(data.length));
            $("#uploadprogressbar").progressBar(percentage);
        });
    }, 5000);
}