const express = require("express");
const session = require("expression-session");
const app = express()
var POST = 5555;
app.use(session({
    secret:'svecw',
    resave:'true',
    saveUninitialized:true
}));
app.get("/",function(req,res){
    req.session.name = 'Hello SVECW!';
    return res.send("Session Set");
});
app.get("/session",function(req,res){
    var name = req.session.name;
    return res.send(name);
});
app.listen(PORT,function(error){
    if(error) throw error
    console.log("Server created Successfully on PORT:",PORT)
});
