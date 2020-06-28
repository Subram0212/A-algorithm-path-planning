# import process_image


def astar(maze, start_pt, end_pt):
    w, h = 8, 8
    sx, sy = start_pt
    ex, ey = end_pt
    node = [None, sx, sy, 0, abs(sx-ex) + abs(sy-ey)]
    close_list = [node]
    created_list = {}
    created_list[sy*w + sx] = node

    while close_list:
        node = close_list.pop(0)
        x = node[1]
        y = node[2]
        l = node[3] + 1
        # k += 1

        neighbours = ((x, y+1), (x, y-1), (x+1, y), (x-1, y))

        for nx, ny in neighbours:
            if nx == ex and ny == ey:
                    path = [(nx, ny)]
                    while node:
                        path.append((node[1], node[2]))
                        node = node[0]
                    return list(reversed(path))
            if 0 <= nx < w and 0 <= ny < h and maze[nx][ny] == 0:
                if ny*w + nx not in created_list:
                    nn = [node, nx, ny, l, l + (abs(nx - ex) + abs(ny - ey))]
                    created_list[ny*w + nx] = nn
                    nni = len(close_list)
                    close_list.append(nn)
                    # sorting using minimum binary heap,
                    while nni:
                        i = (nni - 1) >> 1
                        if close_list[i][4] > nn[4]:
                            close_list[i], close_list[nni] = nn, close_list[i]
                            nni = i
                        else:
                            break
    return []
