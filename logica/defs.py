import cv2
import numpy as np
import math

'''
separeting the disk from the rest of screen and returning a black and white img in RGB scale where the disk is white and the rest is black
'''
def disk_mask(img, disk_lower: tuple[int, int, int], disk_upper: tuple[int, int, int]):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    disk_mask = cv2.inRange(hsv, disk_lower, disk_upper)

    disk_mask = cv2.cvtColor(disk_mask, cv2.COLOR_GRAY2RGB)

    return disk_mask


'''
returning the circles from the input img, use a edge detector to make it better
'''
def get_disk_center(mask, frame):
    edges = cv2.Canny(mask, 100, 70)

    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,2,40,param1=50,param2=10,minRadius=10,maxRadius=50)

    circleCenter = None

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # drawing circle center and perimeter
            # comment this on real application to minimize lag
            cv2.circle(frame, (i[0], i[1]), i[2], (255, 0, 0), 3)
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 0), 3)
            circleCenter = (i[0], i[1])
            break

    return circleCenter


'''
class to save disk current and previous position, make it easy to get necessary information with methods and make all the raycast
'''
class GlobalDisk:
    def __init__(self) -> None:
        self.current_pos = None
        self.prev_pos = None

    def new_pos(self, pos:np.array):
        # setting previous position as current position
        self.prev_pos = self.current_pos
        # updating current position to position received
        self.current_pos = pos

    '''
    return the direction that the disk is going
    '''
    def get_direction(self) -> tuple[int, int]:
        if self.current_pos == None or self.prev_pos == None:
            return None
        # need to converto to int because position is a np.array and it represent values as a unsigned 2 bytes integer
        x0 = int(self.current_pos[0])
        x1 = int(self.prev_pos[0])
        y0 = int(self.current_pos[1])
        y1 = int(self.prev_pos[1])
        return (x0 - x1, y0 - y1)

    # def get_velocity(self) -> int:
    #     if type(self.current_pos) != type(None) and type(self.prev_pos) != type(None):
    #         x, y = (self.get_direction()) ** 2
    #         return np.sqrt(x + y)
    #     return None

    def draw_direction_line(self, img:np.array, color:tuple[int, int, int]):
        direction = self.get_direction()
        if direction == None:
            return
        cv2.line(img, tuple(self.current_pos), tuple(np.array(self.current_pos) + np.array(direction)), color, 2)

    def intersections(self, img:np.array, line_color:tuple[int, int, int], point_color:tuple[int, int, int], line0x:int, line1x:int, defense_line:int, height:int, depth:int):
        #          /--------\
        #          | (def)  |
        #          | ooooo  |
        #          |        |
        #  line0x  |        |   line1x
        #          |        |
        #          |        |
        #          |        |
        #          \--------/
        #            height
        pos = list(self.current_pos)
        direction = self.get_direction()

        # ignoringn cases where previous position isnt set
        if direction is None:
            return None
        if pos[1] < defense_line:
            return None

        direction = list(direction)

        # ignoring case where disk is going to player side
        if direction[1] > 0: return

        for _ in range(depth):
            
            # saving original position of disk or position where disk would collide with wall
            # we just use it to draw, so can be commented on final application
            ori_pos = [i for i in pos]

            px, py = pos
            m = get_angle(direction[0], direction[1])

            # getting what wall disk is going to hit based on its current direction or the direction reflected if it already collided with a wall 
            yline = line1x if direction[0] > 0 else line0x

            # equacao da reta
            y = m * yline + (py - m * px)

            if not (y > height or y < defense_line):
                # point of collision with wall
                pos[1] = int(y)
                pos[0] = yline
                # reflecting direction on wall
                direction[0] = -direction[0]
                            
            # equacao da reta
            x = (defense_line - (py - m * px)) / m

            if not (x < line0x or x > line1x):
                # point of collision with defense line
                pos[0] = int(x)
                pos[1] = defense_line

                # drawing prediction, can be commented on final application
                cv2.line(img, tuple(ori_pos), tuple(pos), line_color, 2)
                cv2.circle(img, tuple(pos), 2, point_color, 5)

                # returning point of collision with defense line
                return pos

            # drawing prediction, can be commented on final application
            cv2.line(img, tuple(ori_pos), tuple(pos), line_color, 2)
            cv2.circle(img, tuple(pos), 2, point_color, 5)


def draw_horizontal_line(img:np.array, y:int, color:tuple[int, int, int]):
    img = cv2.line(img, (0, y), (500, y), color, 2)


def draw_vertical_line(img:np.array, x:int, color:tuple[int, int, int]):
    img = cv2.line(img, (x, 0), (x, 1500), color, 2)

def get_angle(x:int, y:int) -> float:
    if x == 0 or y == 0:
        return np.pi
    return math.atan(y/x)

if __name__ == "__main__":
    GlobalDisk.new_pos((2, 2))
    GlobalDisk.new_pos((4, 4))
    # print(GlobalDisk.get_direction())
    # print(GlobalDisk.get_velocity())
    print(GlobalDisk.get_angle()/3.1415 * 180)
