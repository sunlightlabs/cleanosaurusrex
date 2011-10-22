(function(){
    function on_nudge_success (data, textStatus, jqXHR) {
        dismiss_nudge_dialog();
    }

    function on_nudge_error (jqXHR, textStatus, errorThrown) {
    }

    function on_bone_success (data, textStatus, jqXHR) {
        dismiss_bone_dialog();
    }

    function on_bone_error (jqXHR, textStatus, errorThrown) {
    }

    function confirm_nudge () {
        $("#mask").show();
        $("#overlay").show();
        $("#pop-over").show();
    }

    function dismiss_nudge_dialog () {
        $("#mask").hide();
        $("#overlay").hide();
        $("#pop-over").hide();
    }

    function confirm_bone () {
        $("#mask").show();
        $("#overlay").show();
        $("#pop-over2").show();
    }

    function dismiss_bone_dialog () {
        $("#mask").hide();
        $("#overlay").hide();
        $("#pop-over2").hide();
    }

    $(document).ready(function(){
        var today = Date.today();

        $("#nudge-button").click(function(){
            confirm_nudge();
            return false;
        });

        $("#yea-button").click(function(){
            $.ajax('/api/nudge/',
                   { type: 'post',
                     success: on_nudge_success,
                     error: on_nudge_error });
        });

        $("#nay-button").click(function(){
            dismiss_nudge_dialog();
        });

        $("#bone-button").click(function(){
            confirm_bone();
            return false;
        });

        $("#yea-button2").click(function(){
            $.ajax('/api/bone/',
                   { type: 'post',
                     success: on_bone_success,
                     error: on_bone_error });
        });

        $("#nay-button2").click(function(){
            dismiss_bone_dialog();
        });

        $('a[rel=home]').bind('click', function(ev) {
            ev.preventDefault();
        });

        $('html').bind('touchmove', function(ev) {
            ev.preventDefault();
        });
        
        window.scrollTo(0, 1);

    });
})();

