from collections import deque
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request
import json
import re

malAnimeChartLink = 'https://myanimelist.net/topanime.php'
malAnimeChartPage = urllib.request.urlopen(malAnimeChartLink)
malAnimeChartSoup = BeautifulSoup(malAnimeChartPage, 'html.parser')

topAnimeTag = malAnimeChartSoup.find('a', attrs={'class': 'hoverinfo_trigger fl-l fs14 fw-b'})

topAnimeName = topAnimeTag.string.strip()
topAnimeLink = topAnimeTag.get('href')

queue = deque()
queued = {}

animeGraph = {}

queue.append(topAnimeName)
queued[topAnimeName] = topAnimeLink

while len(queue) != 0:
  animeName = queue.popleft()
  print(animeName)
  
  animeGraph[animeName] = []
  
  animeLink = queued.get(animeName)
  animeLinkCleaned = animeLink[:29] + urllib.parse.quote(animeLink[29:])
  
  recommendationsLinkCleaned = animeLinkCleaned + '/userrecs'
  recommendationsPage = urllib.request.urlopen(recommendationsLinkCleaned)
  recommendationsSoup = BeautifulSoup(recommendationsPage, 'html.parser')
  
  def isAnimeTag(tag):
    return tag.name == 'a' and tag.next_element.name == 'strong' and 'anime' in tag.get('href')
  
  recommendedAnimeTags = recommendationsSoup.find_all(isAnimeTag)
  
  for recommendedAnimeTag in recommendedAnimeTags:
    recommendedAnimeLink = recommendedAnimeTag.get('href')
    recommendedAnimeName = recommendedAnimeTag.string
    animeGraph[animeName].append(recommendedAnimeName)
    if queued.get(recommendedAnimeName) is None:
      queue.append(recommendedAnimeName)
      queued[recommendedAnimeName] = recommendedAnimeLink
      
with open('animeGraph.json', 'w') as fp:
    json.dump(animeGraph, fp)
