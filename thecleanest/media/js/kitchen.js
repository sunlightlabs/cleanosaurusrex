(function(){
    function on_nudge_success (data, textStatus, jqXHR) {
        $("#mask").hide();
        $("#overlay").hide();
    }

    function on_nudge_error (jqXHR, textStatus, errorThrown) {
    }

    function on_bone_success (data, textStatus, jqXHR) {
        alert('Bone given');
    }

    function on_bone_error (jqXHR, textStatus, errorThrown) {
    }

    function popover (data, textStatusm, jqXHR) {
        var frag = document.createDocumentFragment();
        $(frag).html(data);
        $("#yea-button", frag).click(function(){
        });
        $("#popover *").remove();
        $("#popover").append(frag);
        $("#popover").show();
    }

    $(document).ready(function(){
        var today = Date.today();

        $("#nudge-button").click(function(){
            $("#mask").show();
            $("#overlay").show();
            return false;
        });

        $("#yea-button").click(function(){
            $.ajax('/api/nudge/',
                   { type: 'post',
                     success: on_nudge_success,
                     error: on_nudge_error });
        });

        $("#nay-button").click(function(){
            $("#mask").hide();
            $("#overlay").hide();
        });

        $("#bone-button").click(function(){
            $.ajax('/api/bone/',
                   { type: 'post',
                     success: on_bone_success,
                     error: on_bone_error });
        });
    });
})();

