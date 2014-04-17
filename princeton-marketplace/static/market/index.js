$(document).ready(main);

// THIS IS WHERE EXECUTION STARTS
function main(){
  var leftPane = {
    "Home": "",
    "All Buy Postings": "all_buying_posts",
    "All Sell Postings": "all_selling_posts"
  };
  Mustache.tags = ['[[', ']]'];
  
  $(".leftPane").click(function (e){
    var url = leftPane[$(e.target).text()];
    $.getJSON("/" + url, function (data){
      var template = $("script." + url).html();
      var len = data.length;
      for (var i = 0; i < len; i++){
        var ready = Mustache.render(template, data[i]);
        $("tbody." + url).append(ready);
      }
      $("div." + "table-responsive").show();
    });
  });
}
