voice_scripts
=============

Scripts to work with Stephen Hickson's linux voicecommand system:
http://stevenhickson.blogspot.co.uk/2013/05/voice-command-v20-for-raspberry-pi.html

Requires Python (I have 2.7, but you may have success with other versions).


Instructions
============

Edit your voicecommand config file (voicecommand -e) and add commands that run the scripts in this directory.
e.g.
weather forecast==~/your_path_to_this_directory/bbcweather

In the case of the bbcweather script, it passes in a location code (currently Hertford, United Kingdom).  You may wish to customize this - see the script for more details.

Please make your own changes and send them to me, or (preferably) via a github pull request:
https://help.github.com/articles/using-pull-requests

Have fun!

Duncan.
