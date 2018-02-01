#!/usr/bin/python2

from pytube import YouTube
import bs4 as bs
import urllib2 as ur
import html5lib
import sys
import os

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print "Invalid argument"
    sys.exit(0)

playlistAddress = sys.argv[1]

sauce = ur.urlopen(playlistAddress).read()
soup = bs.BeautifulSoup(sauce, "html5lib")

#Get the playlist TITLE
playlistTitle = soup.find("h1", attrs = {"class":"pl-header-title"}).text.strip()

print "Fetching playlist information...\n"

#Create subfolder in /home/erik/Videos/Youtube/
folderPath = "/home/erik/Videos/Youtube/" + playlistTitle + "/"
if not os.path.isdir(folderPath):
    print "Creating location: " + folderPath
    os.makedirs(folderPath)
else:
    print "Saving files to existing location: " + folderPath

downloadedVideos = []
abortedVideos = []

print "\nDownloading...\n"

currentVideoNumber = 1

for td in soup.find_all("td", attrs = {"class" : "pl-video-title"}):
    a = td.find("a")
    if "/watch" in a.get("href"):
        videoAddress = "https://www.youtube.com" + a.get("href")
        yt = YouTube(videoAddress)
        video = yt.filter("mp4")[-1]
        try:
            print str(currentVideoNumber) + ": " + "Filename: " + yt.filename + "\nFormat: " + str(yt.filter("mp4")[-1])
            video.download(folderPath)
            downloadedVideos.append(str(yt.filename))
        except OSError:
            print "DUPLICATE FILENAME FOUND! Aborting download..."
            abortedVideos.append(str(yt.filename))
        currentVideoNumber += 1
        print

print "Successfully downloaded " + str(len(downloadedVideos)) + " videos:"

for i in range(len(downloadedVideos)):
    print str(i + 1) + " : " + str(downloadedVideos[i])
print "\nFailed to download " + str(len(abortedVideos)) + " videos:"
for i in range(len(abortedVideos)):
    print str(i + 1) + " : " + str(abortedVideos[i])

print "\nDownload finished!"