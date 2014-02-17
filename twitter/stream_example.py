"""
Example program for the Stream API. This prints public status messages
from the "sample" stream as fast as possible.

USAGE

  stream-example -t <token> -ts <token_secret> -ck <consumer_key> -cs <consumer_secret>

"""

from __future__ import print_function

import argparse

from twitter.stream import TwitterStream, Timeout
from twitter.oauth import OAuth
from twitter.util import printNicely


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-t',  '--token', help='The Twitter Access Token.')
    parser.add_argument('-ts', '--token-secret', help='The Twitter Access Token Secret.')
    parser.add_argument('-ck', '--consumer-key', help='The Twitter Consumer Key.')
    parser.add_argument('-cs', '--consumer-secret', help='The Twitter Consumer Secret.')
    parser.add_argument('-us', '--user-stream', action='store_true', help='Connect to the user stream endpoint.')
    parser.add_argument('-ss', '--site-stream', action='store_true', help='Connect to the site stream endpoint.')
    parser.add_argument('-to', '--timeout', help='Timeout for the stream (seconds)')
    parser.add_argument('-nb', '--no-block', action='store_true', help='Set stream to non-blocking')
    return parser.parse_args()

def main():
    args = parse_arguments()

    if not all((args.token, args.token_secret, args.consumer_key, args.consumer_secret)):
        print(__doc__)
        return 2

    # When using twitter stream you must authorize.
    auth = OAuth(args.token, args.token_secret, args.consumer_key, args.consumer_secret)
    if args.user_stream:
        stream = TwitterStream(auth=auth, domain='userstream.twitter.com', timeout=args.timeout, block=not args.no_block)
        tweet_iter = stream.user()
    elif args.site_stream:
        stream = TwitterStream(auth=auth, domain='sitestream.twitter.com')
        tweet_iter = stream.site()
    else:
        stream = TwitterStream(auth=auth)
        tweet_iter = stream.statuses.sample()

    # Iterate over the sample stream.
    for tweet in tweet_iter:
        # You must test that your tweet has text. It might be a delete
        # or data message.
        if tweet is None:
            printNicely("-- None --")
        elif tweet is Timeout:
            printNicely("-- Timeout --")
        elif tweet.get('text'):
            printNicely(tweet['text'])

if __name__ == '__main__':
    main()
