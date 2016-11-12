from PIL import Image,ImageDraw
import random

def readfile(filename):
	lines = [line for line in file(filename)]

	# First line is the column titles
	colnames = lines[0].strip().split('\t')[1:]
	rownames = []
	data = []
	for line in lines[1:]:
		p = line.strip().split('\t')

		# First column in each row is the rowname
		rownames.append(p[0])

		# The data for this row is the remainder of the row
		data.append([float(x) for x in p[1:]])
	return rownames, colnames, data

from math import sqrt


def pearson(v1,v2):
  # Simple sums
  sum1=sum(v1)
  sum2=sum(v2)

  # Sums of the squares
  sum1Sq=sum([pow(v,2) for v in v1])
  sum2Sq=sum([pow(v,2) for v in v2])

  # Sum of the products
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/len(v1))
  den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
  if den==0: return 0

  return 1.0-num/den


class bicluster:
  def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
	self.left = left
	self.right = right
	self.vec = vec
	self.id = id
	self.distance = distance


def test(rows,rownames):
  i=len(rows)-1
  print len(rows)
  while i >= 0:
  	print rownames[i]
  	print len(rows[i])
  	i = i-1


def hcluster(rows,distance=pearson):
  distances={}
  currentclustid=-1

  # Clusters are initially just the rows
  clust=[bicluster(rows[i],id=i) for i in range(len(rows))]

  while len(clust)>1:
    lowestpair=(0,1)
    closest=distance(clust[0].vec,clust[1].vec)

    # loop through every pair looking for the smallest distance
    for i in range(len(clust)):
      for j in range(i+1,len(clust)):
        # distances is the cache of distance calculations
        if (clust[i].id,clust[j].id) not in distances:
          distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)
        
        d=distances[(clust[i].id,clust[j].id)]
        
        if d<closest:
          closest=d
          lowestpair=(i,j)
    
    # calculate the average of the two clusters
    mergevec=[
    (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0
    for i in range(len(clust[0].vec))]
    
    
    # create the new cluster
    newcluster=bicluster(mergevec,left=clust[lowestpair[0]],
                          right=clust[lowestpair[1]],
                          distance=closest,id=currentclustid)

    
    # cluster ids that weren't in the original set are negative
    currentclustid-=1
    # delete the two already merged clusters
    del clust[lowestpair[1]] 
    del clust[lowestpair[0]]
    clust.append(newcluster)

  return clust[0]


# Recurtion:
def printclust(clust,labels=None,n=0):
	# indent to make a hierarchy layout
	for i in range(n): print ' ',
	if clust.id<0:
	    # negative id means that this is branch
	    print '-'
	else:
	    # positive id means that this is an endpoint
	    if labels==None: print clust.id
	    else: print labels[clust.id]
	# now print the right and left branches
	if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
	if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)


def rotatematrix(data):
  newdata=[]
  for i in range(len(data[0])):
    newrow=[data[j][i] for j in range(len(data))]
    newdata.append(newrow)
  return newdata
		

# how long is the vertical line?
def getheight(clust):
	# Is this an endpoint? Then the height is just 1
	if clust.left == None and clust.right == None: return 1

	# Otherwise the height is the same of the heights of each branch
	return getheight(clust.left) + getheight(clust.right)

# how long is the horizontal line?
def getdepth(clust):
	# The distance of and endpoint is 0
	if clust.left == None and clust.right == None: return 0

	# The distance of a branch is the greater of its two sides plus its own distance
	return max(getdepth(clust.left),getdepth(clust.right)) + clust.distance

def drawdendrogram(clust, labels, jpeg="clusters.jpg"):
	# height and width
	h = getheight(clust) * 20
	w = 1200
	depth = getdepth(clust)

	# width is fixed, so scale distances accordingly
	scaling = float(w-150)/depth

	# Create a new image with a white background
	img = Image.new('RGB', (w, h), (255, 255, 255))
	draw = ImageDraw.Draw(img)

	# The very left first small horizontal line in the middle of the height
	draw.line((0, h/2, 10, h/2), fill=(0, 0, 0))

	# Draw the first node
	drawnode(draw, clust, 10, (h/2), scaling, labels)
	img.save(jpeg,'JPEG')


def drawkclusters(clust, labels, jpeg="clusters.jpg", size = 20):
	h = len(labels) * size
	w = 600

	# Create a new image with a white background
	img = Image.new('RGB', (w, h), (255, 255, 255))
	draw = ImageDraw.Draw(img)

	# The very left first small horizontal line in the middle of the height
	draw.line((20, h/2, 60, h/2), fill=(0, 0, 0))

	# Draw the first node
	drawnodekclusters(draw, clust, 60, labels, size)
	img.save(jpeg,'JPEG')

def drawnodekclusters(draw, clust, kx, labels, size):
	height = []
	for i in clust:
		height.append(len(i))
	print height

	y1 = height[0] * size / 2
	y2 = len(labels) * size - height[len(clust)-1] * size / 2
	# Vertical line from this cluster to children
	draw.line((kx,y1,kx,y2),fill=(255,0,0))
	
	
	j = 0
	while(j < len(height) - 1):
		# The second very left horizontal line:
		draw.line((kx, y1, 150, y1), fill=(0, 0, 0))
		draw.line((150,y1 + (height[j] - 1) * (size / 2 - 1), 150, y1 - (height[j] - 1) * (size / 2 - 1)),fill=(255,0,0))
		tip = y1 - (height[j] - 1) * (size / 2 - 1)
		for x in range(height[j]):
			draw.line((150, tip, 250, tip), fill=(0, 0, 0))
			draw.text((250+5,tip-7),labels[clust[j][x]],(0,0,0))
			tip += size - 2

		y1 +=  (height[j] + height[j + 1]) * size / 2
		j += 1

	# The last horizontal line of the second very left
	draw.line((kx, y2, 150, y2), fill=(0, 0, 0))

	# The last cluster
	draw.line((150,y2 + (height[j] - 1) * (size / 2 - 1), 150, y2 - (height[j] - 1) * (size / 2 - 1)),fill=(255,0,0))
	
	tip = y2 - (height[j] - 1) * (size / 2 - 1)
	for x in range(height[j]):
		draw.line((150, tip, 250, tip), fill=(0, 0, 0))
		draw.text((250+5,tip-7),labels[clust[j][x]],(0,0,0))
		tip += size - 2





def drawnode(draw,clust,x,y,scaling,labels):
  
  # If this is not an endpoint: there should be line.
  if clust.id<0:
	h1=getheight(clust.left)*20 # vertical line up
	h2=getheight(clust.right)*20 # vertical line down
	top=y-(h1+h2)/2
	bottom=y+(h1+h2)/2

	# the horizontal line length
	ll=clust.distance*scaling

	# Vertical line from this cluster to children
	draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

	# Horizontal line to left item
	draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

	# Horizontal line to right item
	draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

	# Call the function to draw the left and right nodes
	drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
	drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)

  else:
    # If this is an endpoint, draw the item label
    draw.text((x+5,y-7),labels[clust.id],(0,0,0))


def kcluster(rows,distance=pearson,k=4):
  # Determine the minimum and maximum values for each point
  ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows]))
  for i in range(len(rows[0]))]

  # Create k randomly placed centroids
  clusters=[[random.random( )*(ranges[i][1]-ranges[i][0])+ranges[i][0] 
  			for i in range(len(rows[0]))] for j in range(k)]

  lastmatches=None
  for t in range(100):
    print 'Iteration %d' % t
    bestmatches=[[] for i in range(k)]

    # Find which centroid is the closest for each row
    for j in range(len(rows)):
      row=rows[j]
      bestmatch=0
      for i in range(k):
        d=distance(clusters[i],row)
        if d<distance(clusters[bestmatch],row): bestmatch=i
      bestmatches[bestmatch].append(j)

    # If the results are the same as last time, this is complete
    if bestmatches==lastmatches: break
    lastmatches=bestmatches

  # Move the centroids to the average of their members
  for i in range(k):
	avgs=[0.0]*len(rows[0])
	if len(bestmatches[i])>0:
	  for rowid in bestmatches[i]:
	    for m in range(len(rows[rowid])):
	      avgs[m]+=rows[rowid][m]
	  for j in range(len(avgs)):
	    avgs[j]/=len(bestmatches[i])
	  clusters[i]=avgs
	  
  return bestmatches




