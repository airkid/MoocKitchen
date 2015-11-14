$(document).ready(function () {
    $("#show_lear").click(function () {
        $("#show_lear").addClass("active");
        $("#show_com").removeClass("active");
        $("#show_inf").removeClass("active");
        $("#chan_key").removeClass("active");
        $("#completed").hide();
        $("#personal_information").hide();
        $("#change_password").hide();
        $("#learning").show();
    });
    $("#show_com").click(function () {
        $("#show_com").addClass("active");
        $("#show_lear").removeClass("active");
        $("#show_inf").removeClass("active");
        $("#chan_key").removeClass("active");
        $("#learning").hide();
        $("#personal_information").hide();
        $("#change_password").hide();
        $("#completed").show();
    });
    $("#show_inf").click(function () {
        $("#show_inf").addClass("active");
        $("#show_com").removeClass("active");
        $("#show_lear").removeClass("active");
        $("#chan_key").removeClass("active");
        $("#learning").hide();
        $("#completed").hide();
        $("#change_password").hide();
        $("#personal_information").show();
    });
    $("#chan_key").click(function () {
        $("#chan_key").addClass("active");
        $("#show_inf").removeClass("active");
        $("#show_lear").removeClass("active");
        $("#show_com").removeClass("active");
        $("#learning").hide();
        $("#completed").hide();
        $("#personal_information").hide();
        $("#change_password").show();
    });
});

//$.ajaxSetup({
//  dataType: "json",
//  beforeSend: function(xhr, settings){
//      var csrftoken = $.cookie('csrftoken');
//      xhr.setRequestHeader("X-CSRFToken", csrftoken);
//  }
//});


$(document).ready(function () {
    $('#change_pass_form').ajaxForm(
        function (data, status) {
            alert(data['message']);
            $('#blank3').val("");
            $('#blank4').val("");
            $('#blank5').val("");
        });
});

$(document).ready(function () {
    $('#change_info_form').ajaxForm(
        function (data, status) {
            alert(data['message']);
            //把头像换成新的
            $('#user_img').src = data['user_img']
        });
});