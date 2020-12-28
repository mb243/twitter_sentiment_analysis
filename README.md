# Twitter Sentiment Analysis

Perform sentiment analysis on Twitter accounts that you follow

Uses the [Twitter v2 "Early Access" API](https://developer.twitter.com/en/docs/twitter-api/early-access), and requires a developer bearer token.

## Installing

Start by cloning or downloading this repo locally.

Next, install the required Python modules with:

```
pip3 install --user -r requirements.txt
```

## Using

Set your bearer token on the command line:

```
export TWITTER_BEARER_TOKEN="your bearer token here"
```

Next, run the script with:

```
./twitter.py username_to_review
```

## Potential future improvements

- Improve error handling
- Using numpy and pandas for data framing
