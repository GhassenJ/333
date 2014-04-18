$(document).ready(main);

// GLOBAL VARIABLES
var lastDisplay = $("div.home_feed");

// MOUSE-CLICK HANDLERS
function leftPaneHandler(e){
  var url = this.className.split(/\s+/)[1];
  var template = $("script." + url).html();
  $.getJSON("/" + url, function (data){
    $("tbody." + url).empty();
    var len = data.length;
    for (var i = 0; i < len; i++){
      var ready = Mustache.render(template, data[i]);
      $("tbody." + url).append(ready);
    }
    lastDisplay.hide();
    lastDisplay = $("div." + url);
    lastDisplay.show();
  });
}

// THIS IS WHERE EXECUTION STARTS
function main(){
  Mustache.tags = ['[[', ']]'];
  var leftPane = $("a").filter(function (){
    return this.className.match(/leftPane/);
  });
  leftPane.click(leftPaneHandler);
  console.log("done");
}
