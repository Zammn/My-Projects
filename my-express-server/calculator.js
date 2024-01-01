//jshint esversion:6

const express = require("express");
const bodyParser = require("body-parser");
const app = express();
app.use(bodyParser.urlencoded({extended: true}));


app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
})
app.post("/", function(req, res) {
    console.log(req.body);
    var num1 = Number(req.body.num1);
    var num2 = Number(req.body.num1);
    var answer = num1 + num2;

    res.send("The answer is " + answer)
})

app.listen(3000, function() {
    console.log("server has been started!")
})