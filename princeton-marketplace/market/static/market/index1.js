// caching
$.ajaxSetup({cache: true});

// for modularity's sake: displays [data] in the form of [block] inside [frame], and display the first [number].
//BUG: THIS DOESN'T CHECK FOR WHEN THERE IS ONLY ONE POSTING
function display(data, block, frame, number){
    var user_id = {{ user.id }};
   /*console.log(data);*/
   var json = data;
   var count = Object.keys(json).length;
   /*console.log(json);*/
   if (number == 0)
      number = count;
  var buttony;
   for (var i = 0; i < number; i++)
   {
      if (i >= count) break;
      var author_id = json[i]["author"]['id'];
      var post_id = json[i]["id"];
      var url = "{% url 'market:posting_detail' 000 %}".replace(000, post_id);
      var ct = i+1;
      if (user_id === author_id) {
      buttony = '<button type="button">Delete Post</button>';
        console.log("SAME: Here is the YOU:"+user_id+"and here is the author:"+author_id);    }
      else {
      buttony = '<button type="button">Accept Post</button>'; 
        console.log("DIFFERENT: Here is the YOU:"+user_id+"and here is the author:"+author_id);    }
      $('<a class="fancybox" rel="gallery1" data-fancybox-type="ajax"><div id="blocky"> Post'+ post_id + ': ' + json[i]["title"]+'<div style="display:none" class="contents"> <div class = "des">description: '+json[i]["description"]+' </div> <div class = "aut">author: '+json[i]["author"]['username'] + '  </div> <div class = pri>price: ' + json[i]["price"] +' </div> <div class = "til">Category: ' + json[i]["category"]["name"]  + '</div> <div class = "date">date: '+ json[i]["date_posted"] + '</div>'+buttony+' </div></div></a>').appendTo(frame);
   }
};

function home(){
   var user_id = {{ user.id }};
   $.ajax({
      url: "{% url 'market:user_detail' 000 %}".replace(000, user_id),
      dataType: "json",
      success: function(data) {
          var cats = data["categories"];
          var catnum = Object.keys(cats).length;
          // someone play with the percentages here?
          $('#cat1').html("You like " + cats[0]["name"] + "! That is cool. Let us fetch you posts from that category:<br><table><tr><td style='border-width:0px' id='cat1sell'></td><td width='3%'></td><td style='border-width:0px' id='cat1buy'></td></tr></table>");
          $.ajax({
             url: "{% url 'market:category_selling_posts' 000 %}".replace(000, cats[0]["id"]),
             dataType: "json",
             beforeSend:function(){
                // this is where we append a loading image
                $('#cat1sell').html('<div class="loading"><img src="http://glenmartinmusic.com/mustache/wp-content/themes/glenmartin/images/loader.gif" alt="Loading..." width = "50" height = "50" align="center" /></div>');
             }, 
             success: function(data) {
                $('#cat1sell').html("Selling:<br>");
                display(data, 'smallblock', '#cat1sell', 5);
             },
             error:function(){
               // failed request; give feedback to user
               $('#cat1sell').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments. Ajax is not working or you are not logged in. </p>');
             }
          });
          $.ajax({
             url: "{% url 'market:category_buying_posts' 000 %}".replace(000, cats[0]["id"]),
             dataType: "json",
             beforeSend:function(){
                // this is where we append a loading image
                $('#cat1buy').html('<div class="loading"><img src="http://glenmartinmusic.com/mustache/wp-content/themes/glenmartin/images/loader.gif" alt="Loading..." width = "50" height = "50" align="center" /></div>');
             }, 
             success: function(data) {
                $('#cat1buy').html("Buying:<br>");
                display(data, 'smallblock', '#cat1buy', 5);
             },
             error:function(){
                // failed request; give feedback to user
                $('#cat1buy').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments. Ajax is not working or you are not logged in. </p>');
             }
         });
      }
   });
}
var allbuying = null;
var allselling = null;
        $(document).ready(function() {
            var category = []; //titles
            var description = []; //authors
            var author = []; //glats
            var price = []; //glons
            var title = []; //ids
            var date = [];
            $ ('#PopUpModal').on('submit', '.submit-form', function() {
                $.ajax({
                    type: $(this).attr('method'), 
                    url: $(this).attr('action'),
                    data: $(this).serialize(),
                    success: function() { // on success..
                        $('#PopUpModal').modal('hide')
                    },
                    error: function(resp) { // on error..
                        var errors = JSON.parse(resp.responseText);
                        for (error in errors)
                        {
                            var id = '#id_' + error;
                            $(id).parent('p').prepend(errors[error]);
                        }
                    }
                });
                return false;
            });
            $ ("#leftPane ul li").click(function (ev) {
                var texti = $(this).text();
                if (texti === "All Buying Postings") {
                    $.ajax({
                        url: "{% url 'market:all_buying_posts' %}",
                        dataType: "json",
                        beforeSend:function(){
                            // this is where we append a loading image
                            $('#results').html('<div class="loading"><img src="http://glenmartinmusic.com/mustache/wp-content/themes/glenmartin/images/loader.gif" alt="Loading..." width = "50" height = "50" align="center" /></div>');
                        }, 
                        success: function(data) {
                           $('#results').html("");
                           display(data, 'blocky', '#results', 0);
                        },
                        error:function(){
                      // failed request; give feedback to user
                      $('#results').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments. Ajax is not working or you are not logged in. </p>');
                  }
                  });
            }
                else if (texti === "All Selling Postings") {
                    $.ajax({
                        url: "{% url 'market:all_selling_posts' %}",
                        dataType: "json",
                        beforeSend:function(){
                            // this is where we append a loading image
                            $('#results').html('<div class="loading"><img src="http://glenmartinmusic.com/mustache/wp-content/themes/glenmartin/images/loader.gif" alt="Loading..." width = "50" height = "50" align="center" /></div>');
                        }, 
                        success: function(data) {
                           $('#results').html("");
                           display(data, 'blocky', '#results', 0);
                        },
                        error:function(){
                      // failed request; give feedback to user
                      $('#results').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments. Ajax is not working or you are not logged in. </p>');
                  }
                  });
            }
                else if (texti === "HOME") {
                    $('#results').html('<p> Welcome to the Marketplace, the place for you to trade anything you want. </p><br><br> {% if user.is_authenticated %} <font size = "4"> Hi, {{ user.first_name }}. <a href = "accounts/logout">(not {{ user.first_name }} {{ user.last_name }}?)</a> We wish you a happy day.<br><div id="cat1" height = "15%"></div><div id="cat2"></div><div id="cat3"></div>{% else %} Please click on "Login" above to sign in via the Central Authentication system.<br> We support many user-friendly features (categories, hashtags, ..) once you log in!{% endif %}');
                    home(); 
                }
                else if (texti === "CREATE POSTING")
                {
                    ev.preventDefault();
                    var url = "{% url 'market:create_posting' %}"
                    $('#PopUpModal').load(url, function() {
                        $(this).modal('show');
                    });
                    return false;
                }
                else if (texti === "EDIT PROFILE")
                {
                    ev.preventDefault();
                    var url = "{% url 'market:edit_profile' %}"
                    $('#PopUpModal').load(url, function() {
                        $(this).modal('show');
                    });
                    return false;
                }
                else if (texti === "All Categories")
                {
                    $.ajax({
                       url: "{% url 'market:all_categories' %}",
                       dataType: "json",
                       beforeSend:function(){
                          // this is where we append a loading image
                          $('#results').html('<div class="loading"><img src="http://glenmartinmusic.com/mustache/wp-content/themes/glenmartin/images/loader.gif" alt="Loading..." width = "50" height = "50" align="center" /></div>');
                       },
                       success:function(data){
                          var cats = data;
                          var count = Object.keys(cats).length;
                          $('#results').html("");
                          for (var i = 0; i < count; i++)
                          {
                             var cat_name = cats[i]["name"];
                             var divstr = 'cat' + cat_name;
                             $('<li id = "'+divstr+'">'+ cat_name + '</li>').appendTo('#results');
                          };
                          $("#results li").click(function (ev) {
                             var texti = $(this).text();
                             for (var i = 0; i < count; i++)
                             {
                                if (texti === cats[i]["name"]){
                                   $.ajax({
                                      url: "{% url 'market:category_selling_posts' 000 %}".replace(000, cats[i]["id"]),
                                      dataType: "json",
                                      beforeSend:function(){
                                         // this is where we append a loading image
                                         $('#results').html('<div class="loading"><img src="http://glenmartinmusic.com/mustache/wp-content/themes/glenmartin/images/loader.gif" alt="Loading..." width = "50" height = "50" align="center" /></div>');
                                      },
                                      success:function(data2){
                                         $('#results').html('Selling posts for ' + cats[i]["name"] + ':');
                                         display(data2, 'smallblock', '#results', 0);
                                      },
                                      error: function(){
                                         $('#results').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments. Ajax is not working or you are not logged in. </p>');
                                      }
                                   });
                                   $.ajax({
                                      url: "{% url 'market:category_buying_posts' 000 %}".replace(000, cats[i]["id"]),
                                      dataType: "json",
                                      beforeSend:function(){
                                      },
                                      success:function(data2){
                                         $("Hello").appendTo('#results');
                                         display(data2, 'smallblock', '#results', 0);
                                      },
                                      error: function(){
                                         $('#results').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments. Ajax is not working or you are not logged in. </p>');
                                      }
                                   });    
                                   break;
                                }
                             }
                          });
                       },
                       error: function(){
                           $('#results').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments. Ajax is not working or you are not logged in. </p>');
                       }            
                    });
                }
            });
    });
    $(document).on('click', '.fancybox', function() {
        var clicked = $(this);
        var element = clicked.html();
        var div = $('.contents').get(0).innerHTML;
        var content = $(this).find("div[class='contents']").get(0).innerHTML;
        console.log(element);
        console.log(content);
        console.log(div);
        $.fancybox({
            'content': content
        });
    });