#!/usr/bin/python2

from pytube import YouTube
from pytube import exceptions
from os.path import expanduser
import bs4 as bs
import urllib2 as ur
import optparse
import sys
import os


def set_url(u):
    try:
        return ur.urlopen(u).read()
    except ValueError:
        print("Invalid URL format")
        sys.exit(1)


parser = optparse.OptionParser()
parser.add_option("-p", "--playlist", dest="playlistAddress", help="Enter address to playlist", type=str)
parser.add_option("-v", "--video", dest="videoAddress", help="Enter address to video", type=str)

(options, args) = parser.parse_args()

# Exit if none or both params are entered
if (options.playlistAddress is not None and options.videoAddress is not None) or \
        (options.playlistAddress is None and options.videoAddress is None):
    print("Invalid params (choose one)")
    sys.exit(1)

# If playlist is chosen
if(options.playlistAddress is not None):
    playlistAddress = options.playlistAddress
    sauce = set_url(playlistAddress)
    soup = bs.BeautifulSoup(sauce, "html5lib")

    # Get the playlist TITLE
    try:
        playlistTitle = soup.find("h1", attrs={"class": "pl-header-title"}).text.strip()
    except AttributeError:
        print("Not a playlist URL")
        sys.exit(1)
    print("Fetching playlist information...\n")

    # Create subfolder in /home/erik/Videos/Youtube/
    folderPath = expanduser("~") + "/Videos/Youtube/" + playlistTitle + "/"
    if not os.path.isdir(folderPath):
        print("Creating location: " + folderPath)
        os.makedirs(folderPath)
    else:
        print("Saving files to existing location: " + folderPath)

    downloadedVideos = []
    abortedVideos = []

    print("\nDownloading...\n")

    currentVideoNumber = 0

    for td in soup.find_all("td", attrs={"class": "pl-video-title"}):
        a = td.find("a")
        if "/watch" in a.get("href"):
            videoAddress = "https://www.youtube.com" + a.get("href")
            try:
                currentVideoNumber += 1
                video = YouTube(videoAddress)
                video = video.streams.filter(subtype="mp4").all()[0]
                try:
                    print (str(currentVideoNumber) + ": " + "Filename: " + a.text.strip())
                    video.download(folderPath)
                    downloadedVideos.append(str(a.text.strip()))
                except OSError:
                    print("DUPLICATE FILENAME FOUND! Aborting download...")
                    abortedVideos.append(str(video.filename))

            except exceptions.RegexMatchError:
                print("Unable to download from URL: " + videoAddress)

    print("Successfully downloaded " + str(len(downloadedVideos)) + " videos:")

    for i in range(len(downloadedVideos)):
        print (str(i + 1) + " : " + str(downloadedVideos[i]))
    print("\nFailed to download " + str(len(abortedVideos)) + " videos:")
    for i in range(len(abortedVideos)):
        print str(i + 1) + " : " + str(abortedVideos[i])

    print("\nDownload finished!")

if options.videoAddress is not None:
    videoAddress = options.videoAddress
    sauce = set_url(videoAddress)

    try:
        soup = bs.BeautifulSoup(sauce, "html5lib")

        video = YouTube(videoAddress)

        channelName = ""
        for link in soup.find_all("a", {"class": "yt-uix-sessionlink spf-link "}):
            channelName = link.text.strip()

        # Create subfolder in /home/erik/Videos/Youtube/
        folderPath = expanduser("~") + "/Videos/Youtube/" + channelName + "/"
        if not os.path.isdir(folderPath):
            print("Creating location: " + folderPath)
            os.makedirs(folderPath)
        else:
            print("Saving files to existing location: " + folderPath)

        # Fetch video name
        videoName = ""
        for n in soup.find_all("h1", {"class": "watch-title-container"}):
            videoName = n.find("span").text.strip()

        # Start downloading
        print("Downloading: [" + videoName + "]")
        video.streams.filter(subtype="mp4").all()[0].download(folderPath)

    except exceptions.RegexMatchError:
        print("Invalid video URL")







