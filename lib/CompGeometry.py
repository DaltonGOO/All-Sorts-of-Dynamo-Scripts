#Find the center of mass of an irregular object
def findCenterMass(points):
    x = 0
    y = 0
    for point in points:
        x += point[0]*point[2]
        y += point[1]*point[2]
    x = x/sum(point[2] for point in points)
    y = y/sum(point[2] for point in points)
    return [x,y]
def findCenter(points):
    x = 0
    y = 0
    for point in points:
        x += point[0]
        y += point[1]
    x = x/len(points)
    y = y/len(points)
    return [x,y]