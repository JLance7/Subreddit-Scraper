#This scraper downloads posts from listed subreddits in subreddits.txt to the images folder
#imports
import praw
import time
import client_secrets
import urllib
import os

class Scraper():
    #global variables
    how_many_posts = 2
    #options to sort posts by: hot, new, top
    filter_option = 'new'
    reddit = None

    #constructor
    def __init__(self):
        #create reddit instance
        self.reddit = praw.Reddit(
            client_id=client_secrets.id,
            client_secret=client_secrets.secret,
            user_agent="<console>:Downloader",
        )


    #make list of subreddits in subreddits text file
    def getSubreddits(self):
        list = []
        file = open('subreddits.txt','r')
        for line in file.readlines():
            if line != '\n':
                line = line.strip()
                list.append(line)
        return list


    #go through each subreddit in subreddits text file and get the url of top 5 posts
    def getUrls(self, list):
        urls = []
        print('Sorting by: ' + self.filter_option)
        for sub in list:
            print('sub is ' + sub)
            if self.sub_exists(sub):
                subreddit = self.reddit.subreddit(sub)
                print('\nGetting posts from ' + sub)
                count = 0
                keepGoing = True
                while keepGoing:
                    if self.filter_option == 'hot':
                        for post in subreddit.hot():
                            if count == self.how_many_posts:
                                keepGoing = False
                                break
                            time.sleep(0.2)
                            #check if post has image
                            check = post.url[len(post.url) - 3 :].lower()
                            if "jpg" not in check and "png" not in check:
                                continue
                            else:
                                urls.append(post.url)
                                count = count + 1
                    elif self.filter_option == 'new':
                        for post in subreddit.new():
                            if count == self.how_many_posts:
                                keepGoing = False
                                break
                            time.sleep(0.2)
                            check = post.url[len(post.url) - 3 :].lower()
                            if "jpg" not in check and "png" not in check:
                                continue
                            else:
                                urls.append(post.url)
                                count = count + 1
                    elif self.filter_option == 'top':
                        for post in subreddit.top():
                            if count == self.how_many_posts:
                                keepGoing = False
                                break
                            time.sleep(0.2)
                            check = post.url[len(post.url) - 3 :].lower()
                            if "jpg" not in check and "png" not in check:
                                continue
                            else:
                                urls.append(post.url)
                                count = count + 1
            else:
                print('Subreddit: ' + sub + ' does not exist.')
                continue  
        return urls


    #check if subreddit exists
    def sub_exists(self, sub):
        exists = True
        try:
            self.reddit.subreddits.search_by_name(sub, exact=True)
        except Exception:
            exists = False
        return exists


    #print urls for debugging
    def print_urls(self, urls):
        for url in urls:
            print('********')
            print(url)        
        

    #def download images to folder
    def getImages(self, urls):
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
        print('\nFinished')


    def setHowManyPosts(self, num):
        self.how_many_posts = num


    def setFilterOption(self, type):
        self.filter_option = type