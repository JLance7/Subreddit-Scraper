from scraper import Scraper


#main runner demonstrates class calls
def main(Scraper):
    #create object
    scrape = Scraper()

    #set how many posts you want from each subreddit (takes in integer)
    scrape.setHowManyPosts(5)

    #set the filter for grabbing posts (options are: hot, new, top)
    scrape.setFilterOption('hot')

    #get subreddits from text file
    list = scrape.getSubreddits()
    #get urls from subreddits
    urls = scrape.getUrls(list)
    #download images
    scrape.getImages(urls)


main(Scraper)