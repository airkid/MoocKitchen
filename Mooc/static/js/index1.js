$(function () {
    var Accordion = function (el, multiple) {
        this.el = el || {};
        this.multiple = multiple || false;

        // Variables privadas
        var links = this.el.find('.link');
        // Evento
        links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
    }

    Accordion.prototype.dropdown = function (e) {
        var $el = e.data.el;
        $this = $(this),
            $next = $this.next();

        $next.slideToggle();
        $this.parent().toggleClass('open');

        if (!e.data.multiple) {
            $el.find('.submenu').not($next).slideUp().parent().removeClass('open');
        }
        ;
    }

    var accordion = new Accordion($('#accordion'), false);
});

//function getMessage() {
//    course_id = {{course_id}};
//    $.ajax({
//        type: 'get',
//        url: "/get_messages/",
//        data:{'course_id':course_id},
//        success: function (responseData) {
//            $('#messages').html(responseData);
//        }
//    })
//}
function setReference(floorId) {
                        $('#reference_id').val(floorId);
                    }
//$(document).ready(function () {
//    $('#message_form').ajaxForm(
//        function (data, status) {
//            $('#reference_id').val(-1);
//            $('#message_area').val("");
//            getMessage();
//            alert(status);
//        });
//});
//
//$(document).ready(function(){
//    $('#show_talk').click(function(){
//        getMessage();
//    })
//})
