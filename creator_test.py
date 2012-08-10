from RedditAccountCreator import RedditAccountCreator

def main():
    print "starting creation ..."
    creator = RedditAccountCreator("http://www.reddit.com")
    creator.create_account("honkmaster", "ficken123", "stpid@mail.com")
    print "run ended"

if __name__ == "__main__":
    main()