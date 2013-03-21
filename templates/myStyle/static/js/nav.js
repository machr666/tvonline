$(document).ready(function() {
	
    // Elements in document
    var $content = $("#content"),
        $nav = $("#nav"),
        $load = $("#load");
    
    // This function changes the content
    var updatePage = function(state) {
        $content.hide('fast', function() {
            $load.fadeIn('fast');
            $.get(state, function (data) {
                var tempHTML=data.replace(/<script/g, "<dynscript").replace(/<\/script/g, "</dynscript");
	        cnt=$(tempHTML).find("#content").html().replace(/dynscript/g, "script");
		$content.html(cnt);
                $load.fadeOut('normal');
                $content.show('normal');
	    });
        });
    }

    // This will make the backward/forward buttons work
    $.History.bind(function(state) {
        updatePage(state);
    });

});
