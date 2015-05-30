# Word-o-cheat
Tool for cheating in words games

Script allows you to find out all the words from input set of characters.
(at the moment, only for Russian language)

1. wordcheat.py : works as a tool, just wait for loading and type set of characters.
2. wordcheat_server.py : listens to the specified port (localhost:80 by default) and takes GET requests like 
http://server/?=setofchars, returns data array in JSON format.
