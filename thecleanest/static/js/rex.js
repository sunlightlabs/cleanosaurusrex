(function(){
    var display_assignments = function (data, textStatus, jqXHR) {
    };

    var display_ajax_error = function (jqXHR, textStatus, errorThron) {
    };

    $(document).ready(function(){
        var today = Date.today(),
            monday = today.clone().moveToDayOfWeek(1, -1);

        $.ajax('/api/assignment/',
               { data: { 'date_gte': monday.toString('yyyy-MM-dd'),
                         'format': 'json',
                         'limit': 10 },
                 success: display_assignments,
                 error: display_ajax_error 
               });

        $("table#eligibles").tablesorter({
            sortList: [[3,1]],
            textExtraction: function(node){
                console.log(node);
                var value = $(node).attr('data-value');
                if (value != null) {
                    return value;
                } else {
                    return $(node).text();
                }
            }
        });
    });
})();
