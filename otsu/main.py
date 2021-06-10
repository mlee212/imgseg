from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# load and convert image into grayscale
gryscl = (Image.open('rels_b.jpg').convert('LA'))

# print(gryscl.format, gryscl.size, gryscl.mode)
# gryscl.show()

# create dictionary of pixel luminosity values and counts
pixV = {}

for y in range(gryscl.height):
    for x in range(gryscl.width):
        pixel, fill = gryscl.getpixel((x,y))
        if pixel not in pixV.keys():
            pixV[pixel] = 1
        else:
            pixV[pixel] = pixV[pixel] + 1
print(pixV)

# create a bar chart of luminosity values and counts
x1 = []
y1 = []

for key, value in pixV.items():
    x1.append(key)
    y1.append(value)

print(x1)
print(y1)

plt.bar(x1, y1, align='center', alpha=0.5)

plt.show()

# Calculate Otsu's variance threshold
variances = []

for i in range(1,len(y1)):
    wb = 0
    wf = 0
    leftsum = 0
    rightsum = 0
    leftprod = 0
    rightprod = 0
    leftmean = 0
    rightmean = 0
    leftcnt = 0
    rightcnt = len(y1)
    
    while(leftcnt < i):
        leftprod = leftprod + x1[i] * y1[i]
        leftsum = leftsum + y1[i]
        leftcnt = leftcnt + 1
    while(rightcnt >= i):
        j = len(y1)-i
        rightprod = rightprod + x1[j] * y1[j]
        rightsum = rightsum + y1[j]
        rightcnt = rightcnt - 1
    
    
    wb = leftsum / len(y1)
    wf = rightsum / len(y1)
    leftmean = leftprod / leftsum
    rightmean = rightprod / rightsum

    variances.append(wb * wf * (leftmean - rightmean)**2)
    # print(i, ": ")
    # print('wb: ', wb)
    # print('wf: ', wf)
    # print('lmean: ', leftmean)
    # print('rmean: ', rightmean)


print('variances: ', variances)

print(variances.index(max(variances)), ':', max(variances))

print('threshold:', x1[variances.index(max(variances))])

# modify pixel values according to threshold
for y in range(gryscl.height):
    for x in range(gryscl.width):
        pixel, fill = gryscl.getpixel((x,y))
        # print('x,y', x, y)
        # print('pixel:',pixel)
        # print('sup')
        if pixel > x1[variances.index(max(variances))]:
            gryscl.putpixel((x,y), (255,255))
        else:
            gryscl.putpixel((x,y), (0,255))

# show image
gryscl.show()