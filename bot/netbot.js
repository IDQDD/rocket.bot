const { driver } = require('@rocket.chat/sdk');
//const respmap = require('./reply');
const rmap = require('./funcs');

// customize the following with your server and BOT account information
const HOST = process.env.ROCKET_HOST || 'http://rocket.acme';
const USER = process.env.ROCKET_USER || 'easybot';
const PASS = process.env.ROCKET_PASS || 'mypasswrd';
const BOTNAME = process.env.ROCKET_BOTNAME || 'easybot';  // name the bot response to
const SSL = true;  // server uses https ?
const ROOMS = ['sandbox'];

var myuserid;
// this simple bot does not handle errors, different message types, server resets 
// and other production situations 

const runbot = async () => {
    const conn = await driver.connect( { host: HOST, useSsl: SSL})
    myuserid = await driver.login({username: USER, password: PASS});
    const roomsJoined = await driver.joinRooms(ROOMS);
    console.log('joined rooms');

    // set up subscriptions - rooms we are interested in listening to
    const subscribed = await driver.subscribeToMessages();
    console.log('subscribed');

    // connect the processMessages callback
    const msgloop = await driver.reactToMessages( processMessages );
    console.log('connected and waiting for messages');

    // when a message is created in one of the ROOMS, we 
    // receive it in the processMesssages callback

    // greets from the first room in ROOMS 
    const sent = await driver.sendToRoom( BOTNAME + ' is listening ...',ROOMS[0]);
    console.log('Greeting message sent');
}

// callback for incoming messages filter and processing
const processMessages = async (err, message, messageOptions) => {
    if (!err) {
        // filter our own message
        if (message.u._id === myuserid) return;
        // can filter further based on message.rid
        const roomname = await driver.getRoomName(message.rid);
        let response;
        if (message.msg.toLowerCase().startsWith('@' + BOTNAME)) {
            const msg = message.msg.substr(BOTNAME.length + 2); // 2 means '@' + 'space'
            const cli = msg.split(" ");
            
            console.log('msg: |'+msg+'|');
            
            if (cli[0] in rmap) { // commands with args
                const elem = rmap[cli[0]];
                if (typeof elem === 'function')
                    response = await elem(cli.slice(1));
                else 
                    response = elem;
            } else {
                response = message.u.username + ', @' + BOTNAME + 'пока не умеет в метод(' + msg + ').\n' +
                    'Для списка команд напишите: @' + BOTNAME + ' ***help***';
            }
        }
        console.log(`response = ${response}`);
        if (response) {
            const sentmsg = await driver.sendToRoom(response, roomname);
        }
    }
} 

runbot()
