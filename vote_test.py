#!/usr/bin/env python
from RedditVotingSession import RedditVotingSession
from TorCycler import TorCycler
import time

#vote target
vote_url = 'http://www.reddit.com/r/mac/comments/y27yl/using_ipad_2_as_primary_monitor/c5ro16c'
vote_type = 'comment'
vote_direction = 'down'

#proxy config
PROXY_HOST = "localhost"
PROXY_PORT = 9050


def main():
    credentials = open(".credentials", "r").readlines()
    accounts = []
    for line in credentials:
        creds_arry = line.strip().split()
        if len(creds_arry) < 2:
            continue
        username = creds_arry[0]
        password = creds_arry[1]
        accounts.append({'username' : username, 'password' : password})
    tor_cycler = TorCycler() 
    for account in accounts:
        tor_cycler.cycle()
        rs = RedditVotingSession("http://www.reddit.com")
        success = rs.login(account['username'], account['password'])
        if not success: 
            print "login failed for user: " + account['username']
            continue
        
        #here we could loop over a list of submissions to vote on
        if vote_type == 'submission':
            if vote_direction == 'up':
                success = rs.upvote_submission(vote_url)
            if vote_direction == 'down':
                success = rs.downvote_submission(vote_url)
        if vote_type == 'comment':
            if vote_direction == 'up':
                success = rs.upvote_comment(vote_url)
            if vote_direction == 'down':
                success = rs.downvote_comment(vote_url)
        if success:
            print "vote succeeded for user " + account['username']
        else:
            print "vote failed for user " + account['username']
        
        time.sleep(1) #give enough time for shit to settle down ...
        rs.quit_browser()
        #now it would be a good time to cycle your TOR ip :]

if __name__ == "__main__":
    main()
