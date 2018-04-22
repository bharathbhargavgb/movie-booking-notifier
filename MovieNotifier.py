import urllib2
from bs4 import BeautifulSoup
import time
from datetime import datetime
import boto3
import sys

# Create an SNS client
# Use IAM user credentials available in console.aws.amaozn.com in IAM section
client = boto3.client(
    "sns",
    aws_access_key_id="ACCESS_KEY_ID",
    aws_secret_access_key="SECRET_ACCESS_KEY",
    region_name="us-west-2"
)

retry = 0
movieTitle = ""

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        movieTitle = "avengers".lower()
    else:
        movieTitle = sys.argv[1].lower()

    while True:

        url = "https://www.jazzcinemas.com/"
        #url = "file:///Users/baaskab/projects/Movie%20Notifier/jazz.html"
        page = urllib2.urlopen(url)

        soup = BeautifulSoup(page, 'html.parser')
        imax = soup.find('div', attrs = {'id':'imaxmovielistdiv'})

        for atag in imax.findAll('a'):
            movieName = str(atag['title']).lower()
            if movieTitle in movieName:
                print "Found!"
                # Publish the nmessage
                client.publish (
                    PhoneNumber="+9197XXXXXX16",
                    Message="AVENGERS INFINITY WAR ticket booking opened!!!"
                )
            else:
                print "Not found"

        # Retry every minute
        print "Retrying in a minute..."
        time.sleep(60)

        print ("[" + str(datetime.now()) + "] Retry #" + str(retry))
        retry += 1