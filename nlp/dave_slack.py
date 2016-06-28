from slackclient import SlackClient
import time
import os as os

#read exported token value from terminal
token = os.environ.get('SLACK_BOT_TOKEN')
sc = SlackClient(token)
print(sc.api_call("api.test"))
print(sc.api_call("channels.info", channel="1234567890"))
print(sc.api_call(
    "chat.postMessage", channel="#general", text="Hello from the Wetterfee Python bot! :tada: Waiting for inputs...",
    username='Wetterfee', icon_emoji=':robot_face:'
))


print("Beginning RTM connection listen loop")
if sc.rtm_connect():
    while True:
        print(sc.rtm_read())
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")
