1. This bot removes all posts from a single subreddit that are older than a customizable date.

1. Both "delete_posts.py" and "botconfig.ini" must be in the same folder.

1. If you don't have Python installed then you must [download](https://www.python.org/downloads/) it from the official Python website. Do not download Python via any other link.

1. Install PRAW, the Python wrapper for the Reddit API. Basically it's as simple as typing "pip install praw" on the command line. Use [this link](https://pythonprogramming.net/introduction-python-reddit-api-wrapper-praw-tutorial/) for more detailed instructions.

1. You have to create a reddit app to gain access to the Reddit API aka PRAW. To do this you must use old reddit.

- Go to your preferences, click the "app" tab and click "create app" or "create new app" if you've created other apps in the past.

- Complete the form in a manner similar to [this screen shot](https://imgur.com/8tOTVQP), but obviously customize it to suit your own needs.

- I use example.com for the redirect URL because it's an example domain that doesn't actually do anything.

1. Open botconfig.ini with a text editor and set each of the items to whatever is appropriate for the sub you're going to run it on and save it.

- You must define: client_id, client_secret, username, password, subreddit, and date_range.

- Note that date_range defines the most recent date to start removing later posts from.

- user_agent is the name of your bot. The default name is Reddit_PostDeletionBot, but you can change it to whatever you prefer.

1. Preparing to run the bot:

- On the command line change directories to the one where the script lives.

- Type "delete_posts.py" on the command line and press enter.

- PRAW limits things like post removals to 30 requests per minute so depending on how many posts you need to remove this process can take a long time.

- As it's running you'll see the title of each post it's removing. When it's done you'll see how many posts it removed.
