$(document).ready(main);

// GLOBAL VARIABLES
var last_url = "home_feed";
var current_url = "home_feed";
var user_id;

// MOUSE-CLICK HANDLERS

// handles click on any menu item on the leftPane
function leftPaneHandler(e){
  var url = this.className.split(/\s+/)[1];
  var template = $("script." + url).html();
  $.getJSON("/" + url, function (data){
    $("tbody." + url).empty();
    var len = data.length;
    for (var i = 0; i < len; i++){
      var ready = Mustache.render(template, data[i]);
      $("tbody." + url).append(ready);
      $("button#post-" + data[i]["id"]).click(openPostHandler);
    }
    $("div." + current_url).hide();
    $("div." + url).show();
    last_url = current_url;
    current_url = url;
  });
}

// handles opening of any post for viewing (not editing)
// this post can be originated by the current user or some other user
function openPostHandler(e){
  var url = "posting_detail";
  var id = this.id.split(/\-+/)[1];
  // template
  $.getJSON("/" + url + "/" + id, function (data){
    var ready = $("div." + url).html();
    $("div." + url).empty();
    // var ready = Mustache.render(template, data);
    $("div." + url).html(ready);
    $("div." + current_url).hide();
    $("div." + url).show();
    last_url = current_url;
    current_url = url;
    $("a#back").show();
  });
}

// handles clicks on the "back" button in the topBar
// this button is displayed only sometimes, so you might not see it on the home screen
// IMPORTANT: the implementation right now is VERY bad, it has to be improved using some tricky code and a stack
function backHandler(e){
  $("div." + current_url).hide();
  $("div." + last_url).show();
  current_url = last_url;
  last_url = "home_feed";
  $("a#back").hide();
}

// THIS IS WHERE EXECUTION STARTS
function main(){
  var user_id = parseInt($("script#user_id").html());
  Mustache.tags = ['[[', ']]'];
  var leftPane = $("a").filter(function (){
    return this.className.match(/leftPane/);
  });
  leftPane.click(leftPaneHandler);
  $("a#back").click(backHandler);
  console.log("done");
}
