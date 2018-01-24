youtube-search
This program searches for the most viewed videos on the word landslide in the past 24 hours on youtube.
And prints out the top ten videos.

Since youtube time uses the format rfc3339 I installed a library that handles the date in that form.
Use "pip install rfc3339" to install the library.
Use "pip install --upgrade google-api-python-client" to install googles python api client
Now just run python mostViewed.py