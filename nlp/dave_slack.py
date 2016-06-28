from slackclient import SlackClient

token = "xoxb-52893672196-IhQ98ue1ZRgmn2TWIZuAbrqF"      # found at https://api.slack.com/web#authentication
sc = SlackClient(token)
print(sc.api_call("api.test"))
print(sc.api_call("channels.info", channel="1234567890"))
print(sc.api_call(
    "chat.postMessage", channel="#general", text="Hello from the Wetterfee Python bot! :tada:",
    username='Wetterfee', icon_emoji=':robot_face:'
))
