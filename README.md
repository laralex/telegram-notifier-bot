To host on Linux:

Install python and libs:
```
sudo apt update
sudo apt install python3 python3-pip -y
/usr/bin/python3 -m pip install python-telegram-bot[job-queue]
```

Save telegram bot token to file `token.txt`
Save channel id into file `channel_id.txt`
Save chat id of your user into file `notification_sink_chat_id.txt`, this id can be found by messaging `@userinfobot`

### Test run
Test run in terminal:
```
python3 bot.py
```

Access bot from telegram:
@laralex_notifier_bot

### Deploy upon startup of Linux machine:

Enable and start
```
cp systemctl.service /etc/systemd/system/laralex_notifier_bot.service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable laralex_notifier_bot
sudo systemctl start laralex_notifier_bot
```

Check status
```
sudo systemctl status laralex_notifier_bot
```
