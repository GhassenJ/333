var express = require('express');
var app = express();
app.get('/', function(req, res){
    res.send('Hello World\n');
});
app.get('/index.html', function(req, res) {
    res.sendfile('public/index_Json_parse.html', {root: __dirname })
});
app.get('/data.json', function(req, res) {
    res.sendfile('public/data.json', {root: __dirname })
});
app.get('/data2.json', function(req, res) {
    res.sendfile('public/data2.json', {root: __dirname })
});
app.get('/data3.json', function(req, res) {
    res.sendfile('public/posting_detait_1.json', {root: __dirname })
});
app.get('/data4.json', function(req, res) {
    res.sendfile('public/posting_detait_12.json', {root: __dirname })
});
app.listen(8000);