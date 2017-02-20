function post(x, id) {
    if (x.length > 200) {
        x = '\n*' + x
    }
    document.getElementById('input').value = (id ? ":" + id + " ": "") + x;
    document.getElementById("sayit-button").click();
}
var last_message = "";

function f() {
    for (var i of document.getElementsByClassName("pending"))
        for (var j of i.children)
            for (var k of j.children)
                if (k.innerHTML == "retry") k.click();

    var e = [].slice.call(document.getElementsByClassName("message")).slice(-1)[0];
    console.log(e.children);
    var a = [].slice.call(document.getElementsByClassName("content")).slice(-1)[0].textContent;
    if (a == last_message) return;
    last_message = a;

    var username = "Feeds";
    for (var i of document.getElementsByClassName("username")) username = i.innerHTML;
    var message_id = e.id.match(/\d+/).slice(-1)[0];

    //if (/@(?!ETH)/i.test(a)) return; // Avoid messages that ping other users
    if (username == "SanBot") return; // Avoid your own messages
 
 var xhr = new XMLHttpRequest();

var tag = document.createElement("script");
tag.src = 'http://localhost:8090/'+a+'/'+parseInt(message_id);

document.getElementsByTagName("head")[0].appendChild(tag)
}

post("SanBot™ *Client* (re)started.");

setInterval(f, 500);