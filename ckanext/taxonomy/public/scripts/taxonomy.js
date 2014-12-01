
$("#tree").jstree({
    "plugins" : ["themes","html_data","ui","crrm"],
     "themes" : {
        "theme" : "default",
        "dots" : false,
        "icons" : false
    },

}) .bind("loaded.jstree", function (event, data) {
    $('#tree').show();
});


