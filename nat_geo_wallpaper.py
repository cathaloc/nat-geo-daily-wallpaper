#!/usr/bin/python

from appscript import *
from bs4 import BeautifulSoup
import urllib
import datetime
import os

url = "http://www.nationalgeographic.com/photography/photo-of-the-day/"
today = datetime.date.today().strftime("%Y_%m_%d")
path_of_the_day = os.path.expanduser("~/Pictures/nat_geo_photo_of_day/") + today + ".jpg"

def __main__():
  if os.path.isfile(path_of_the_day):
    print "You already downloaded today's photo. Check back tomorrow!"
    return

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
  se = app('System Events')
  desktops = se.desktops.display_name.get()
  for d in desktops:
    desk = se.desktops[its.display_name == d]
    desk.picture.set(mactypes.File(path_of_the_day))

__main__()