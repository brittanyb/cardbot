#!/bin/bash

systemctl --user restart cardbot.service

# Include this file in the root of the repo and the way I've set it up will
# automatically run this script when you push new commits to it, so you don't
# have to manually restart the bot.
# When you make this file, also run the following in the ubuntu bash prompt:
# `chmod u+x deploy.sh`
# (without the backticks)
# this makes the script executable for the owner of the file.