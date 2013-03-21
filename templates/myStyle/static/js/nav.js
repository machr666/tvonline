$(document).ready(function() {
	
    // Elements in document
    var $content = $("#content"),
        $nav = $("#nav"),
        $load = $("#load"),
        $data = " #content";
    
    // This function changes the content
    var updatePage = function(state) {
        $content.hide('fast', function() {
            $load.fadeIn('fast'); 
            $content.load(state+$data,'',function() {
                    $load.fadeOut('normal');
                    $content.show('normal');
            })
        });
    }

    // This will make the backward/forward buttons work
    $.History.bind(function(state) {
        updatePage(state);
    });

});
