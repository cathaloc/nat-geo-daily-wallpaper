#!/usr/local/bin/python

from appscript import *
from bs4 import BeautifulSoup
import urllib
import datetime
import os
import subprocess

url = "http://www.nationalgeographic.com/photography/photo-of-the-day/"
today = datetime.date.today().strftime("%Y_%m_%d")
path_of_the_day = os.path.expanduser("~/Pictures/nat_geo_photo_of_day/") + today + ".jpg"

def __main__():
  if os.path.isfile(path_of_the_day):
    print "You already downloaded today's photo. Check back tomorrow!"

  file = download_image()
  set_image_as_background()

def download_image():
  r = urllib.urlopen(url).read()
  soup = BeautifulSoup(r, "html.parser")
  url_el = soup.findAll("meta", { "property" : "og:image" })
  image_url = url_el[0]['content']

  title_el = soup.findAll("meta", { "property" : "og:title"})
  image_title = title_el[0]['content']

  desc_el = soup.findAll("meta", { "property" : "og:description"})
  image_desc = desc_el[0]['content']

  urllib.urlretrieve(image_url, path_of_the_day)


def set_image_as_background():
  script =  """
  tell application "System Events"
    repeat with aDesktop in desktops
      tell aDesktop
        set picture to """ + '"' + path_of_the_day + '"' + """
      end tell
    end repeat
  end tell
  """
  proc = subprocess.Popen(['osascript', '-'],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
  stdout_output = proc.communicate(script)[0]
  print stdout_output, type(proc)

__main__()