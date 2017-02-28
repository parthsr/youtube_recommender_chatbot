from __future__ import unicode_literals
import youtube_dl
import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import time
from slackclient import SlackClient
import shutil
import requests
import unirest
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        print channels_call['channels']
        return channels_call['channels']
    return None

def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='parthbot',
    )



def youtube_vid(text):

    query = urllib.quote(text)
    url = "https://www.youtube.com/results?search_query=" + query
    new_url=""
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html,"html.parser")
    counter=1
    urls=[]
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        new_url='https://www.youtube.com' + vid['href'] 
        urls.append(new_url)
        counter = counter+1
        if(counter==6):
            break
    return urls


'''ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ydl_opts={}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([new_url])
'''

def m():
    if slack_client.rtm_connect():
        while True:
             a= slack_client.rtm_read()
             print a
             if a:
                    if(a[0]['type']=='message'):
                          text=a[0]['text']
                          urls=youtube_vid(text)
                          for url in urls:
                            print url
                            send_message(<channel_id>,url)
                            time.sleep(5)
                          break

             time.sleep(1)
    else:
        print 'Connection Failed, invalid token?'

m()


    
