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
  
  // Coloring the side pane. It's intuitive..but could be buggy. Can someone confirm? - bumsoo
  var color = colorHandler(url);
  var oldcolor = colorHandler(current_url);
  if (oldcolor == color) {
    $("."+oldcolor + " current").removeClass("current");
  }
  else {
   $("."+oldcolor).removeClass("current");
  }
  $("."+color).addClass("current");
  
  // Add header to home_feed when we come back to home.
  // I'm not entirely sure if this home pane is necessary, but it will be if we implement search.
  if (url == "home_feed") {
    if (user_id)
    {
      homeHandler();
    }
    $("div." + current_url).hide();
    $("div." + url).show();
    last_url = current_url;
    current_url = url;
    return;
  }
  else {
    $("div.page-head").hide();
  }
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

// Receives a pane and returns its assigned color. We need the class name of the color
// to determine which one should be "shown" at a specific moment.
// pane here refers to one of the following:
// home_feed, all_selling_posts, all_buying_posts, my_open_posts, my_closed_posts, my_responded_posts.
// MY CATEGORY HAS NOT BEEN IMPLEMENTED YET
function colorHandler(pane){
   switch (pane) {
      case "home_feed": return "nred";
      case "all_selling_posts": return "nblue";
      case "all_buying_posts": return "ngreen";
      case "my_open_posts": return "nlightblue";
      case "my_closed_posts": return "nlightblue";
      case "my_responded_posts": return "nviolet";
      default: return "norange";
   }
}

// handles the home case. Hopelessly not modular, I'll try to make it more friendly by tmrw - bumsoo
function homeHandler(){
   $("div.page-head").show(); // show header
   // recent sell postings
   $.getJSON("/all_selling_posts", function (data){
      $("tbody.home_recent_sell").empty();
      var len = data.length;
      for (var i = 0; i < 5; i++){
         if (i >= len) break;
         var template = $("script.home_feed").html();
         var ready = Mustache.render(template, data[i]);
         $("tbody.home_recent_sell").append(ready);
         $("button#post-" + data[i]["id"]).click(openPostHandler);
      }
   });
   // recent buy postings
   $.getJSON("/all_buying_posts", function (data){
      $("tbody.home_recent_buy").empty();
      var len = data.length;
      for (var i = 0; i < 5; i++){
         if (i >= len) break;
         var template = $("script.home_feed").html();
         var ready = Mustache.render(template, data[i]);
         $("tbody.home_recent_buy").append(ready);
         $("button#post-" + data[i]["id"]).click(openPostHandler);
      }
   });
   
   var url = "home_feed";
   var userdata;
   $("div.home_feed_categories").html("");
   // get user data
   $.getJSON("/user_detail/" + user_id, function(data){
      var cats = data["categories"]; // user categories
      var catnum = Object.keys(cats).length;
      for (var i = 0; i < catnum; i++)
      {
         var catid = cats[i]["id"];
         var catname = cats[i]["name"];
         var sellframe = 'home_' + catid + '_sell';
         var buyframe = 'home_' + catid + '_buy';
         $("div.home_feed_categories").append('<div class="col-md-6"><div class="widget wgreen"><div class="widget-head"><div class="pull-left">'+catname+' Sell Postings</div><div class="widget-icons pull-right"><a href="#" class="wminimize"><i class="fa fa-chevron-up"></i></a><a href="#" class="wclose"><i class="fa fa-times"></i></a></div><div class="clearfix"></div></div><!-- Widget content --><div class="widget-content"><table class="table table-bordered "><thead><tr><th>Title</th><th>Price</th><th>From</th><th>Expires</th><th></th></tr></thead><tbody class='+sellframe+'></tbody></table></div></div></div>'); // this looks very complicated, but this essentially adds a widget. THere is a correctly tabbed/indented version for those of you interested.
         $.getJSON("/category_selling_posts/" + catid, function(data){
            $("tbody." + sellframe).empty();
            var len = data.length;
            for (var i = 0; i < 5; i++){
               if (i >= len) break;
               var template = $("script.home_feed").html();
               var ready = Mustache.render(template, data[i]);
               $("tbody." + sellframe).append(ready);
               $("button#post-" + data[i]["id"]).click(openPostHandler);
            }
         });
         $("div.home_feed_categories").append('<div class="col-md-6"><div class="widget wviolet"><div class="widget-head"><div class="pull-left">'+catname+' Buy Postings</div><div class="widget-icons pull-right"><a href="#" class="wminimize"><i class="fa fa-chevron-up"></i></a><a href="#" class="wclose"><i class="fa fa-times"></i></a></div><div class="clearfix"></div></div><!-- Widget content --><div class="widget-content"><table class="table table-bordered "><thead><tr><th>Title</th><th>Price</th><th>From</th><th>Expires</th><th></th></tr></thead><tbody class='+buyframe+'></tbody></table></div></div></div>'); // this looks very complicated, but this essentially adds a widget. If someone wants to know he can ask me..
         $.getJSON("/category_buying_posts/" + catid, function(data){
            $("tbody." + buyframe).empty();
            var len = data.length;
            for (var i = 0; i < 5; i++){
               if (i >= len) break;
               var template = $("script.home_feed").html();
               var ready = Mustache.render(template, data[i]);
               $("tbody." + buyframe).append(ready);
               $("button#post-" + data[i]["id"]).click(openPostHandler);
            }
         });
      }
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
  user_id = (parseInt($("script#user_id").html())).toString();
  Mustache.tags = ['[[', ']]'];
  var leftPane = $("a").filter(function (){
    return this.className.match(/leftPane/);
  });
  leftPane.click(leftPaneHandler);
  $("a#back").click(backHandler);
  console.log("done");
  if (user_id)
  {
   homeHandler();
  }
}
