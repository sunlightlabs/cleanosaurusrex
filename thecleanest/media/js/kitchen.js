(function(){
    function on_nudge_success (data, textStatus, jqXHR) {
        alert('Nudged');
    }

    function on_nudge_error (jqXHR, textStatus, errorThrown) {
    }

    function on_bone_success (data, textStatus, jqXHR) {
        alert('Bone given');
    }

    function on_bone_error (jqXHR, textStatus, errorThrown) {
    }

    function popover (data, textStatusm, jqXHR) {
        $("#popover *").remove();
        $("#popover").append($(data));
        $("#popover").show();
    }

    $(document).ready(function(){
        var today = Date.today();

        $("#nudge-button").click(function(){
            $.ajax('/kitchen/popover', { success: popover });
            return false;
//            $.ajax('/api/nudge/',
//                   { type: 'post',
//                     success: on_nudge_success,
//                     error: on_nudge_error });
        });

        $("#bone-button").click(function(){
            $.ajax('/api/bone/',
                   { type: 'post',
                     success: on_bone_success,
                     error: on_bone_error });
        });
    });
})();

