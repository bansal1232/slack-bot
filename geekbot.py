import os
import requests
import time
import wolframalpha

from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
wolfram_client = wolframalpha.Client(os.environ.get('WOLFRAM_ID'))

def parse_slack_output(message):
    msg_list = message
    if msg_list and len(msg_list) > 0:
        for msg in msg_list:
            if msg and 'text' in msg and AT_BOT in msg['text']:
                return msg['text'].split(AT_BOT)[1].strip().lower(), msg['channel']
    return None, None

def handle_command(command, channel):
    # print command
    try:
        res = wolfram_client.query(command)
        answer = next(res.results).text
        slack_client.api_call("chat.postMessage", channel=channel,
                                text=answer, as_user=True)
    except:
        slack_client.api_call("chat.postMessage", channel=channel,
                                text="Some error occured", as_user=True)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("GeekBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
