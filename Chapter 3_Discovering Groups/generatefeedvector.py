import feedparser
import re

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
	#Parse the feed
	d = feedparser.parse(url)
	wc = {}

	# Loop over all the entries
	for e in d.entries:
		if 'summary' in e: summary = e.summary
		else: summary = e.description

		# Extract a list of words
		words = getwords(e.title + ' ' + summary)
		for word in words:
			wc.setdefault(word, 0)
			wc[word] += 1
	try:
		# In case there is no title: (spend a lot time debug this :-( )
		if d.feed.title == '':
			print url
		return d.feed.title, wc
	except AttributeError:
		print url

def getwords(html):
	# Remove all the HTML tags
	txt = re.compile(r'<[^>]+>').sub('', html)

	# Split words by all non-alpha characters
	words = re.compile(r'[^A-Z^a-z]+').split(txt)

	# Convert to lowercase
	return [word.lower() for word in words if word!='']


apcount = {}
wordcounts = {}
feedlist = 0
for feedurl in file('feedlist.txt'):
	title, wc = getwordcounts(feedurl)
	wordcounts[title]=wc
	for word, count in wc.items():
		apcount.setdefault(word, 0)
		# If one word appears more than once in a url, then append it in the apcount list
		if count > 1:
			apcount[word] += 1
	# Number of urls in the `feedlist.txt`
	feedlist += 1


wordlist=[]
for w,bc in apcount.items():
	# The fraction of one word that appears in the urls
    frac=float(bc)/feedlist
    # Eliminate the most common words like `a` or `the` and the most uncommon words
    if frac>0.1 and frac<0.5: wordlist.append(w)
out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word) 
out.write('\n')
for blog,wc in wordcounts.items():
    out.write(blog)
    print blog
    for word in wordlist:
        if word in wc: out.write('\t%d' % wc[word])
        else: out.write('\t0')
    out.write('\n')
 




