const express = require("express");
const https = require("https");
const bodyParser = require("body-parser");
const app = express();
app.use(bodyParser.urlencoded({extended: true}));

app.get("/", function(req, res){
    res.sendFile(__dirname + "/index.html");
});

app.post("/", function(req, res){
    const query = req.body.cityName;
    const apiKey = "0fc6f1aab70113a26ffe17fde5f712d5";
    const unit = "metric";
    const url = "https://api.openweathermap.org/data/2.5/weather?q=" + query + "&appid=" + apiKey +"&units=" + unit;

    https.get(url, function(response) {
        console.log(response.statusCode);

        response.on("data", function(data) {
            const weatherData =  JSON.parse(data)
            console.log(weatherData);
            const temp = weatherData.main.temp;
            console.log(temp);
            const description = weatherData.weather[0].description;
            console.log(description);
            const icon = weatherData.weather[0].icon;
            const imageURL = "https://openweathermap.org/img/wn/" + icon + "@2x.png";
            res.write("<h1>Weather currently is " + description + ".</h1>");
            res.write("<h1>The temperature in " + query + " right now is " + temp + " degrees Celcius.</h1");
            res.write("<img src=" + imageURL +">");
            res.send();

        })
    })

});

app.listen(3000, function(){
    console.log("Server is running on port 3000");
})