import dotenv from 'dotenv';
dotenv.config();
import express from "express";
import bodyParser from "body-parser";
import ejs from "ejs";
import mongoose from "mongoose";
import session from 'express-session';
import passport from 'passport';
import passportLocalMongoose from 'passport-local-mongoose';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import findOrCreate from 'mongoose-findorcreate';
// import bcrypt, { hash } from "bcrypt";
// import encrypt from "mongoose-encryption";
// import md5 from "md5";
// const saltRounds = 10;

const app = express();
const port = 3000;

app.set("view engine", "ejs"); // Set the view engine to EJS
app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
  secret: "Our little secret",
  resave: false,
  saveUninitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());

mongoose.connect("mongodb://127.0.0.1:27017/userDB", { useNewUrlParser: true });


const userSchema = new mongoose.Schema ({
  email: String,
  password: String,
  googleId: String,
  secret: String,
});

userSchema.plugin(passportLocalMongoose);
userSchema.plugin(findOrCreate);
// userSchema.plugin( encrypt, {secret: process.env.SECRET, encryptedFields: ['password'] });
const User = new mongoose.model("User", userSchema);

passport.use(User.createStrategy());
passport.serializeUser(function(user, done) {
  done(null, user.id);
});
passport.deserializeUser(function(id, done) {
  User.findById(id)
    .then(user => {
      done(null, user);
    })
    .catch(err => {
      done(err, null);
    });
});
passport.use(new GoogleStrategy({
  clientID: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET,
  callbackURL: "http://localhost:3000/auth/google/secrets",
  userProfileURL: "https://www.googleapis.com/oauth2/v3/userinfo"
},
function(accessToken, refreshToken, profile, cb) {
  console.log(profile);
  User.findOrCreate({ googleId: profile.id }, function (err, user) {
    return cb(err, user);
  });
}
));

app.get("/", function (req, res) {
  res.render("home.ejs");
});

app.get("/auth/google",
  passport.authenticate("google", { scope: ["profile"] }
));

app.get("/auth/google/secrets", 
  passport.authenticate('google', { failureRedirect: '/login' }),
  function(req, res) {
    res.redirect("/secrets");
});

app.get("/login", function (req, res) {
  res.render("login.ejs");
});

app.get("/submit", function(req, res){
  if (req.isAuthenticated()){
    res.render("submit");
  } else {
    res.redirect("/login");
  }
});

app.post("/submit", function (req, res) {
  const submittedSecret = req.body.secret;
  console.log(req.user);
  
  User.findById(req.user.id)
    .then((foundUser) => {
      if (foundUser) {
        foundUser.secret = submittedSecret;
        return foundUser.save();
      }
    })
    .then(() => {
      res.redirect("/secrets");
    })
    .catch((err) => {
      console.log(err);
    });
});

app.get("/logout", function(req, res){
  req.logout(function() {
    res.redirect("/");
  });
});

app.get("/register", function (req, res) {
  res.render("register.ejs");
});

app.get("/secrets", async function (req, res) {
  try {
    const foundUsers = await User.find({ "secret": { $ne: null } });

    if (foundUsers) {
      res.render("secrets", { usersWithSecrets: foundUsers });
    }
  } catch (err) {
    console.log(err);
  }
});


//passport
app.post("/login", async function(req, res){
  const user = new User({
    username: req.body.username,
    password: req.body.password,
  });
  req.login(user, function(err){
    if(err){
      console.log(err);
    } else {
      passport.authenticate("local")(req, res, function(){
        res.redirect("/secrets");
      });
    }
  });
});

//passport
app.post("/register", async function(req, res){
  User.register({username: req.body.username}, req.body.password, function(err, user){
    if(err){
      console.log(err);
      res.redirect("/register");
    }else{
      passport.authenticate("local")(req, res, function(){
        res.redirect("/secrets");
      });
    }
  });
});
// hashing 
// app.post("/register", async function (req, res) {
//   try {
//     const hash = await bcrypt.hash(req.body.password, saltRounds);
//     const newUser = new User({
//       email: req.body.username,
//       password: hash
//     });
    
//     await newUser.save();
//     res.render("secrets.ejs");
//   } catch (err) {
//     console.error(err);
//   }
// });

//hashing
// app.post("/login", function(req, res) {
//   const username = req.body.username;
//   const password = req.body.password;

//   User.findOne({ email: username })
//     .then(foundUser => {
//       if (foundUser) {
//         bcrypt.compare(password, foundUser.password, function(err, result) {
//           if (err) {
//             console.error(err);
//             res.send("An error occurred while logging in");
//           } else {
//             if (result === true) {
//               res.render("secrets.ejs");
//             } else {
//               res.send("Invalid username or password");
//             }
//           }
//         });
//       } else {
//         res.send("Invalid username or password");
//       }
//     })
//     .catch(err => {
//       console.error(err);
//       res.send("An error occurred while logging in");
//     });
// });

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
