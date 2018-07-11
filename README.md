## Python recursive crawler

### Required Packages:
* requests
* BeautifulSoup

### Info
It's a python beautifulSoup crawler created for **parsing main content without any knowledge of what would the html structure be like**. We designed a recursive function `recursive_get_content` to contruct a dictionary mapping different kind of **tag node** to their contents, then we select the longest one as the `main content` node.

### Example Usage
Original Link: http://bookmaker-info.com/en/episode-59
![](https://cdn.steemitimages.com/DQmUeRSQCLi9TatH9ySbdYHRqmAA9BSgp5NVbWhroKGPfZW/image.png)


```
python crawler.py http://bookmaker-info.com/en/review_10bet
# print(c)
```

> In this episode of the Bookmaker Podcast, Art Eftekhari a.k.a. Mr. Bookmaker starts in the US as the final two teams in the NBA (Golden State Warriors & Cleveland Cavaliers) are set to do battle on the hardwood for the fourth straight year. Checking in with US-friendly bookmaker in , Art highlights what betting lines are out as we are set to tip-off another highly anticipated NBA Finals. And even though the NBA Finals are front and center, Mr. Bookmaker also dives into some intriguing wagering opportunities courtesy of UK bookie  as we countdown the days until the World Cup in Russia. Will Mohamed Salah make an appearance on the pitch for Egypt? What about the odds for him to land the back of the net? Art mentions this and more in this podcast!And if you haven’t already, be sure to subscribe to The Bookmaker Podcast with Art Eftekhari on Apple Podcasts or Stitcher by clicking on the respective logos below.


### Future work:
* Adjust **request** to avoid being banned
* Add tag whitelist so tags like `<font>` or `<h2>` won't be treated like a "content node"
