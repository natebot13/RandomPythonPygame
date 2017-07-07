~~~ Welcome to the MTG with friends client! ~~~

mtgclient.py version 0.1 - Initial release

It really is just a basic chat and image sharing application, but I wrote it
with the desired intent of being able to play MTG over the internet with my friends.

Currently it only supports two players, but, technically up to 6 people can connect,
with all the same functionality.

In order to run, use python 2.x.x. I don't know why it doesn't work with python3, but
while I figure that out, it works with 2

Start with:
python mtgclient.py

This basic start will automatically connect to my personal server. If you want to run
your own, you'll have to run the chatserver.py on a host machine, forward the port: 30736
and run the clients with arguments:

python mtgclient.py <serverIP/address> <PORT>

Once loaded, open chat with 't' and type '/help'
You'll get this:

/help for this help info.
/nick <nickname> to change your nickname.
Buttons:
t: opens chat
a, d: look through history of your sent images
q, e: look through history of other player's sent iamges
space: take a snapshot
f: send snapshot
s: save the entire screen into an image

That's all for now. have fun!