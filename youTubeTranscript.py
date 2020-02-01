#taken from: https://pypi.org/project/youtube-transcript-api/
#taken from: https://www.promptcloud.com/blog/how-to-scrape-youtube-data-using-python/

#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import json
import ast
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlparse

from youtube_transcript_api import YouTubeTranscriptApi

# For ignoring SSL certificate errors

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


textToSearch = 'github'
query = urllib.parse.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
    print('https://www.youtube.com' + vid['href'])
    print("\n")
    url = 'https://www.youtube.com' + vid['href']
    url_data = urlparse(url)
    query = urllib.parse.parse_qs(url_data.query)
    video_id = query["v"][0]

    # Making the website believe that you are accessing it using a mozilla browser

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    # Creating a BeautifulSoup object of the html page for easy extraction of data.

    soup = BeautifulSoup(webpage, 'html.parser')
    html = soup.prettify('utf-8')
    video_details = {}
    other_details = {}

    for span in soup.findAll('span',attrs={'class': 'watch-title'}):
        video_details['TITLE'] = span.text.strip()

    for script in soup.findAll('script',attrs={'type': 'application/ld+json'}):
            channelDesctiption = json.loads(script.text.strip())
            video_details['CHANNEL_NAME'] = channelDesctiption['itemListElement'][0]['item']['name']

    for div in soup.findAll('div',attrs={'class': 'watch-view-count'}):
        video_details['NUMBER_OF_VIEWS'] = div.text.strip()

    for button in soup.findAll('button',attrs={'title': 'I like this'}):
        video_details['LIKES'] = button.text.strip()

    for button in soup.findAll('button',attrs={'title': 'I dislike this'}):
        video_details['DISLIKES'] = button.text.strip()

    for span in soup.findAll('span',attrs={'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}):
        video_details['NUMBER_OF_SUBSCRIPTIONS'] = span.text.strip()

    hashtags = []
    for span in soup.findAll('span',attrs={'class': 'standalone-collection-badge-renderer-text'}):
        for a in span.findAll('a',attrs={'class': 'yt-uix-sessionlink'}):
            hashtags.append(a.text.strip())
    video_details['HASH_TAGS'] = hashtags


    # retrieve the available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, ['en'])   #list_transcripts
    #transcript_list = transcript_list.find_transcript(['en'])

    # iterate over all available transcripts
    for transcript in transcript_list:

        # fetch the actual transcript data and then display the text attribute in the list
        lyrics = (transcript.fetch()) #Returns a list of dictionaries
        for i in range (1,len(lyrics)):
            print(lyrics[i]['text'])

    links = []
    links.append(url)
    Title = []
    Title.append(video_details['TITLE'])
    print(video_details)

    dict = {'Link': links, 'Description' : Title}
    df=pd.DataFrame(dict)
    df.to_csv("KB_video.csv", index=False)


