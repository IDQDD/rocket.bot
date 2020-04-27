
const deck = [
"\uD83C\uDCA7", "\uD83C\uDCA8", "\uD83C\uDCA9", "\uD83C\uDCAA", "\uD83C\uDCAB", "\uD83C\uDCAC", "\uD83C\uDCAD", "\uD83C\uDCA1",
"\uD83C\uDCB7", "\uD83C\uDCB8", "\uD83C\uDCB9", "\uD83C\uDCBA", "\uD83C\uDCBB", "\uD83C\uDCBC", "\uD83C\uDCBD", "\uD83C\uDCB1",
"\uD83C\uDCC7", "\uD83C\uDCC8", "\uD83C\uDCC9", "\uD83C\uDCCA", "\uD83C\uDCCB", "\uD83C\uDCCC", "\uD83C\uDCCD", "\uD83C\uDCC1",
"\uD83C\uDCD7", "\uD83C\uDCD8", "\uD83C\uDCD9", "\uD83C\uDCDA", "\uD83C\uDCDB", "\uD83C\uDCDC", "\uD83C\uDCDD", "\uD83C\uDCD1"]

const rmap = {
    "hi" : "hey",
    "thanks" : "You are welcome",
    "bot" : "Come'on - of course NO!! :robot:",
    "bye" : "See ya ... :mask:",
    "привет": "сам привет",
    "func1": func1,
    "meme": meme,
    "deck": get_deck,
    "round": get_hands,
    "zabbix": zabgraf,
    "acl": check_acl,
    "md": check_md,
};
// help method that returns a set of keys
rmap.help = function() {return Object.keys(rmap).join(', ');}

// functions
function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        let n = Math.floor(Math.random() * i);
        [arr[i], arr[n]] = [arr[n], arr[i]];
    }
    return arr;
}

function get_deck(){
    return '# ' + shuffle(deck).join(' ');
}

function get_hands() {
    const allcards = shuffle(deck);
    const hand1 = allcards.slice(0, 10);
    const hand2 = allcards.slice(10, 20);
    const hand3 = allcards.slice(20, 30);
    const prikup = allcards.slice(30);

    return '# И: ' + hand1.join(' ') +
        '\n# А: ' + hand2.join(' ') +
        '\n# К: ' + hand3.join(' ') +
        '\n# прикуп: ' + prikup.join(' ');
}

function func1(args) { 
    return args.join("-");
}

// Use: @netbot acl from=any to=10.1.2.0/24 [port=3389] [proto=tcp] 
// rule is based on a batfishe's HeaderConstraints class params
// https://batfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints
// srcIps (str) – Source location/IP
// dstIps (str) – Destination location/IP
// dstPorts – Destination ports as list of ranges, (e.g., "22,53-99")
// ipProtocols – List of well-known IP protocols (e.g., TCP, UDP, ICMP)

function check_acl(args) {
    const jkeys = ["srcIps", "dstIps", "dstPorts", "ipProtocols"]
    const jObj = {};

    if (2 > args.length || args.length > 4) {
        return ":robot: Incorrect argument numbers!\nUse: @BOTNAME acl from=any to=10.1.2.0/24 [port=3389] [proto=tcp]";
    }
    
    args.forEach((el, index) => {
        if (el.includes("=")) {
            jObj[jkeys[index]] = el.split("=")[1];
        }
    });

    if (args.length != Object.keys(jObj).length) {
        return ":robot: Incorrect Format!\nUse: @BOTNAME acl from=any to=10.1.2.0/24 [port=3389] [proto=tcp]";
    }

    return JSON.stringify(jObj);
}

function meme() {
    return {
        "text": "ooops!", "emoji": ":poop:",
        "attachments": [
            {
                "color": "#00AA00",
                "text": "мемчик",
                "image_url": "https://bostonglobe-prod.cdn.arcpublishing.com/resizer/Oyo4TykIQr-wDW3ztz1XsFYa18s=/1024x0/arc-anglerfish-arc2-prod-bostonglobe.s3.amazonaws.com/public/Y5GUIDYVWJGVFP5MWNYJR5375I.png",
            }
        ]
    }
}
function zabgraf() {
    return {
        "text": "Проблемы Zabbix",
        "attachments": [
            {
                "color": "#00AA00",
                "text": "Проблемы Zabbix",
                //"collapsed": true,
                "message_link": "https://zabgraf.vbrr.ru/render/d-solo/bV5WXWqZk/zabbix-problemy?orgId=1&panelId=2&height=800",
                "image_url": "https://zabgraf.vbrr.ru/render/d-solo/bV5WXWqZk/zabbix-problemy?orgId=1&panelId=2&height=800",
            }
        ]
    }
}

function check_md() {
    return `|    | Node   | Filter_Name   | Flow                                                  | Action   | Line_Content                          | Trace                                                |
    |---:|:-------|:--------------|:------------------------------------------------------|:---------|:--------------------------------------|:-----------------------------------------------------|
    |  0 | n7k1   | VL20_OUT      | start=n7k1 [10.2.1.88:0->10.1.2.214:80 TCP length=20] | PERMIT   | 300 permit ip 10.2.1.0/24 10.1.2.0/24 | - Matched line 300 permit ip 10.2.1.0/24 10.1.2.0/24 |
    |  1 | n7k2   | VL20_OUT      | start=n7k2 [10.2.1.88:0->10.1.2.214:80 TCP length=20] | PERMIT   | 300 permit ip 10.2.1.0/24 10.1.2.0/24 | - Matched line 300 permit ip 10.2.1.0/24 10.1.2.0/24 |`;
}


//module.exports = respmap;
module.exports = rmap;
