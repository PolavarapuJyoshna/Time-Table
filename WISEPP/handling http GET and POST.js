var http = require("http");
var url = require("url");
let server = http.createServer(function(req,res){
    if(req.method == "GET"){
        res.writeHead(200,{"Content-Type":"text/html"});
        var requrl = url.parse(req.url,true).query;
        var name = requrl.name;
        var email = requrl.email;
        var address = requrl.address;
        console.log(address);
        console.log(email);
        console.log(name);
        res.write("<html><body><p>"+name+""+email+""+address+"</p></body></html>");
        res.end();
    }
    else if(req.method == "POST"){
        var body = "";
        req.on("data",function(chunck){
            body += chunck;
        });
        req.on("end",function(){
            res.writeHead(200,{"Content-Type":"text/html"});
            res.end(body);
        })
    }
}).listen(3032);
console.log("Server is running at 127.0.0.1:3032...");