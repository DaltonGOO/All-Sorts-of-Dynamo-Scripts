

x_lists = IN[0]
y_lists = IN[1]

OUT = []
for x_nums, y_nums in zip(x_lists, y_lists):
    points = []
    for x in x_nums:
        for y in y_nums:
            #create a point
            point = Point.ByCoordinates(x, y, 0)
            points.append(point)
    OUT.append(points)