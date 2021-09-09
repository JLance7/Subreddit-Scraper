#This scraper downloads posts from listed subreddits in subreddits.txt to the images folder
#imports
import praw
import time
import client_secrets
import urllib
import os

#global variables
how_many_posts = 2
filter_option = 'hot'


#run everything as a script
def main():
    #establish reddit instance with tokens
    reddit = praw.Reddit(
        client_id=client_secrets.id,
        client_secret=client_secrets.secret,
        user_agent="<console>:Downloader",
    )

    #get subreddits from text file
    list = getSubreddits()
    #get urls from subreddits
    urls = getUrls(reddit, list)
    #download images
    getImages(urls)
    

#make list of subreddits in subreddits text file
def getSubreddits():
    list = []
    file = open('subreddits.txt','r')
    for line in file.readlines():
        if line != '\n':
            line = line.strip()
            list.append(line)
    return list


#go through each subreddit in subreddits text file and get the url of top 5 posts
def getUrls(reddit, list):
    global how_many_posts
    original_posts = how_many_posts
    urls = []
    for sub in list:
        how_many_posts = original_posts
        if sub_exists(reddit, sub):
            subreddit = reddit.subreddit(sub)
            print('\nGetting posts from ' + sub)
            count = 0
            keepGoing = True
            while keepGoing:
                for post in subreddit.new():
                    if count == how_many_posts:
                        keepGoing = False
                        break
                    time.sleep(0.2)
                    #check if post has image
                    check = post.url[len(post.url) - 3 :].lower()
                    if "jpg" not in check and "png" not in check:
                        #print('did not pass jpg or png test')
                        #print('the bad url is: ' + post.url)
                        continue
                    else:
                        #print('the accepted url is: ' + post.url)
                        urls.append(post.url)
                        count = count + 1
        else:
            print('Subreddit: ' + sub + ' does not exist.')
            continue  
    return urls


#check if subreddit exists
def sub_exists(reddit, sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except Exception:
        exists = False
    return exists


#print urls for debugging
def print_urls(urls):
    for url in urls:
        print('********')
        print(url)        


#def download images to folder
def getImages(urls):
    i = 0
    #count number of images in images folder
    list = os.listdir('images') 
    number_files = len(list)
    start = number_files
    for url in urls:
        start = start + 1
        check = url[-3:]
        if check == 'jpg':
            fileName = str(start) + ".jpg"
        else:
            fileName = str(start) + ".png"

        full_path = "images/" + fileName
        urllib.request.urlretrieve(url, full_path)
        


main()