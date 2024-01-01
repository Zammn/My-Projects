/* esversion: 6 */

import express from "express";
import bodyParser from "body-parser";


const app = express();
app.use(bodyParser.urlencoded({extended: true}));

app.get("/", function(req, res) {
    const today = new Date();
    const day = today.getDay();

    let type = "a weekday";
    let adv = "it's time to work hard";

    if (day === 0 || day == 6) {
        type = "the weekend";
        adv = "it's time to have some fun";
    }


    res.render("index.ejs", { dayType: type, advice: adv});
});


app.listen(3000, function(){
    console.log("Server started on port 3000");
});