import cv2
import numpy as np
import time
import img_traversing
import astar_search
from skimage.metrics import structural_similarity as ssim


def main(image_file):
    global result_1
    occupied_grids = []
    planned_path = {}
    # Read the image
    image = cv2.imread(image_file)
    (winW, winH) = (60, 60)

    obstacles = []
    index = [1, 1]
    blank_image = np.zeros((60, 60, 3), np.uint8)
    list_images = [[blank_image for i in range(8)] for i in range(8)]
    maze = [[0 for i in range(8)] for i in range(8)]

    # traversing through each grid blocks of the image and store the average color of each grid
    for(x, y, window) in img_traversing.sliding_window(image, stepSize=60, windowSize=(winW, winH)):
        clone = image.copy()
        cv2.rectangle(clone, (x, y), (x + winW, y+winH), (0, 0, 0), -1)
        crop_image = image[x:x+winW, y:y+winH]
        list_images[index[0]-1][index[1]-1] = crop_image.copy()

        average_color_per_row = np.average(crop_image, axis=0)
        average_color_per_box = np.average(average_color_per_row, axis=0)
        average_color_per_box =np.uint8(average_color_per_box)

        # if the grid is not white completely, store the grids with coloured objects in a list
        if(any(i <= 240 for i in average_color_per_box)):
            maze[index[0]-1][index[1]-1] = 1
            occupied_grids.append(tuple(index))

        # put those grids with black obstacles in a separate obstacles' list
        if(any(i <= 20 for i in average_color_per_box)):
            obstacles.append(tuple(index))

        cv2.imshow('Window', clone)
        cv2.waitKey(1)
        time.sleep(0.05)

        index[1] += 1
        if index[1] > 8:
            index[0] += 1
            index[1] = 1

    list_of_colored_grids = [n for n in occupied_grids if n not in obstacles]

    for startimage in list_of_colored_grids:
        img_1 = list_images[startimage[0]-1][startimage[1]-1]

        for grid in [n for n in list_of_colored_grids if n != startimage]:
            img = list_images[grid[0]-1][grid[1]-1]

            image_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
            image_2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            s = ssim(image_1, image_2)

            # if structural similarity index is greater than 0.9, those grids with same objects' shape match each other
            if s > 0.9:
                # perform A* search
                result = astar_search.astar(maze, (startimage[0]-1, startimage[1]-1), (grid[0]-1, grid[1]-1))

                list2 = []
                for i in result:
                    if grid in planned_path.keys():
                        continue
                    else:
                        x, y = i[0]+1, i[1]+1
                        list2.append(tuple((x, y)))
                        _result = list(list2[1:-1])
                        result_1 = list(list2[:])

                # join those two objects of same shape with a line
                while result_1:
                    first_co_ord = result_1.pop(0)
                    if result_1:
                        last_co_ord = result_1.pop(0)
                        x_, y_ = first_co_ord
                        x_1, y_1 = last_co_ord
                        cv2.line(image, (((x_*winW) - 30), ((y_*winW) - 30)), (((x_1*winH) - 30), ((y_1*winH) - 30)),
                                 (0, 0, 0), 2)
                        cv2.imshow('Window', mat=image)
                        result_1.insert(0, last_co_ord)

                if not result:
                    planned_path[startimage] = list(['NO PATH', [], 0])

                # store the co-ordinates of paths joining those two same objects inside a list
                planned_path[startimage] = list([str(grid), _result, len(_result)+1])

    for obj in list_of_colored_grids:
        if obj not in planned_path:
            planned_path[obj] = list(['NO MATCH', [], 0])

    return occupied_grids, planned_path


if __name__ == "__main__":

    image_filename = 'Own_made_image1.jpg'
    occupied_path, planned_path = main(image_filename)
    print("Occupied places are: ")
    print(occupied_path)
    print("Planned path is: ")
    print(planned_path)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
