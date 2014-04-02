var express = require('express');
var app = express();
app.get('/', function(req, res){
    res.send('Hello World\n');
});
app.get('/index.html', function(req, res) {
    res.sendfile('public/index_Json_parse.html', {root: __dirname })
});
app.get('/:myname', function(req, res) {
    res.sendfile('public/'+req.params.myname, {root: __dirname })
});
app.get('/fancybox/:myname', function(req, res) {
    res.sendfile('public/fancybox/'+req.params.myname, {root: __dirname })
});
app.get('/data4.json', function(req, res) {
    res.sendfile('public/posting_detait_12.json', {root: __dirname })
});
app.listen(8000);