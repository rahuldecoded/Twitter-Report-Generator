import tweepy
import json

consumer_key = 'your consumer key'
consumer_secret = 'your consumer secret'

access_token = 'access token'
access_token_secret = 'access token secret'

# initialize the client
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)


'''
    :STRUCTURE:
    userDetails = {
        "minute1": {
            "user1": count1, 
            "user2": count2}, 
        "minute2": {
            "user3": count3}
    }
'''
usersDetails = {}



'''
    :STRUCTURE:
    linkDetails = {
        "minute1": {
            "domain1": count1"
        }
    }
'''
linkDetails = {}

class MyStreamListener(tweepy.StreamListener):
    global usersDetails
    global linkDetails
    
    def get_links_report(self, data):
        '''
            The function to get the domain used in the tweets

            Parameter:
            :data: JSON data

        '''
        try:
            if data['entities']['urls']:
                shortenedLink = data['entities']['urls'][0]['url']
                domain = data['entities']['urls'][0]['expanded_url'].split('/')[2]
                return (shortenedLink, domain)

            elif 'quoted_status' in data:
                shortenedLink = data['quoted_status']['entities']['urls'][0]['url']
                domain = data['quoted_status']['entities']['urls'][0]['expanded_url'].split('/')[2]
                return (shortenedLink, domain)

            elif 'extended_tweet' in data:
                shortenedLink = data['extended_tweet']['entities']['urls'][0]['url']
                domain = data['extended_tweet']['entities']['urls'][0]['expanded_url'].split('/')[2]
                return (shortenedLink, domain)

            elif 'retweeted_status' in data:
                if 'extended_tweet' in data['retweeted_status']:
                    shortenedLink = data['retweeted_status']['extended_tweet']['entities']['urls'][0]['url']
                    domain = data['retweeted_status']['extended_tweet']['entities']['urls'][0]['expanded_url'].split('/')[2]
                    return (shortenedLink, domain)
                else:
                    return None
            else:
                return None    #No links Found

        except KeyError as key_error:
            return None

        except IndexError as index_error:
            return None

    
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        
        '''
            User Report
        '''
        try:
            time = data['created_at']
            username = data['user']['name']
            minute = time.split(':')[1]
            if not usersDetails:
                usersDetails[minute] = { username: 1}

            elif minute not in usersDetails:
                print('\n*******\n')
                print(minute, end=" - ")
                print(len(usersDetails))
                print('*****User Report*****')
                
                
                # prints user report every minute
                print_user_report = {}
                # print_user_report = {"username": twert_count}
                for _minute, userDetail in usersDetails.items():
                    for userName, tweetCount in userDetail.items():
                        if userName in print_user_report:
                            print_user_report[userName] += tweetCount
                        else:
                            print_user_report[userName] = tweetCount
                for userName, tweetcount in print_user_report.items():
                    print(userName + ": " + str(tweetCount))                              
                
                # to check the limit of pipe reached to 5, if yes then delete the last 5th minute record
                # and push the latest record
                if len(usersDetails) == 5:
                    remove = int(minute) - 5
                    if remove < 0:
                        remove = 60 + remove
                    del(usersDetails[str(remove).zfill(2)])
                    
                usersDetails[minute] = {username: 1}
                
            else:
                if username not in usersDetails[minute]:
                    usersDetails[minute][username] = 1
                else:
                    usersDetails[minute][username] += 1
                            


            '''
                Links Report
            '''
            if not linkDetails:

                link_report = self.get_links_report(data)
                if link_report:
                    link, domain = link_report
                    linkDetails[minute] = {domain: 1}
                else:
                    pass
                    
            elif minute not in linkDetails:
                print_link_report = {} 
                total_links_count = 0
                for _minute, link_detail in linkDetails.items():
                    for domain, linkCount in link_detail.items():
                        if domain not in print_link_report:
                            print_link_report[domain] = linkCount
                        else:
                            print_link_report[domain] += linkCount
                        total_links_count += 1
                print('\n*****Links Report*****')
                print('Total links used: ' + str(total_links_count))
                
                reports = print_link_report
                reports = [(k, reports[k]) for k in sorted(reports, key=reports.get, reverse=True)]
                
                for report in reports:
                    print(report[0] + ": " + str(report[1]))
                    
                if len(linkDetails) == 5:
                    remove = int(minute) - 5
                    if remove < 0:
                        remove = 60 + remove
                    del(linkDetails[str(remove).zfill(2)])
                    
                link_report = self.get_links_report(data)
                if link_report:
                    link, domain = link_report
                    linkDetails[minute] = {domain: 1}
                else:
                    linkDetails[minute] = {}
                    
            else:
                link_report = self.get_links_report(data)
                if link_report:
                    link, domain = link_report
                    if domain not in linkDetails[minute]:
                        linkDetails[minute][domain] = 1
                    else:
                        linkDetails[minute][domain] += 1
                else:
                    pass
                
        except KeyError as key_error:
            print(key_error)
            
        except IndexError as index_error:
            print(index_error)
            
        

        
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        
        
myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

keyword = input("Enter the keyword")
myStream.filter(track=[keyword])

