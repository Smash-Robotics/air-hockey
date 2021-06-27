from defs import *
import cv2
import numpy as np
import pyautogui

# simulador = False
simulador = True

if __name__ == "__main__":

	# configs
	defense_line_y = 200
	lateral_line0_x = 30
	lateral_line1_x = 450
	disk_lower = (  0, 100, 100) # HSV
	disk_upper = ( 20, 255, 255) # HSV

	if not simulador:
		cap = cv2.VideoCapture(0)

	disk = GlobalDisk()
	
	while True:
		
		if simulador:
			# if we are using the simuator, screen record the area where the game appears and converting from BGR to RGB
			img = np.array(pyautogui.screenshot(region=(1200, 200, 500, 750)))
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		else:
			# in case of real table, use webcam, if cv2 version < 4, need to convert from BGR to RGB
			ret, img = cap.read()

		# masking the disk from the rest of the img
		mask = disk_mask(img, disk_lower, disk_upper)

		# finding circles on the img and returning the first one center`s, drawing on img the circle and its center
		# problably will need to change the parameters with the real table
		center = get_disk_center(mask, img)
		
		# if find the disk, set it as the new position
		if center != None:
			disk.new_pos(center)

		# drawing map important things
        # comment this on real application to minimize lag
		draw_horizontal_line(img, defense_line_y, (250, 0, 255))
		draw_vertical_line(img, lateral_line0_x, (250, 0, 255))
		draw_vertical_line(img, lateral_line1_x, (250, 0, 255))

		# making raycast and seeing where it intersects with the "defense line", the raycast reflects of walls as in a perfeitamente elastica collision	
		# returns None if didnt find a point	
		p = disk.intersections(img, (255, 255, 255), (0, 170, 255), lateral_line0_x, lateral_line1_x, defense_line_y, 900, 4)
		print(p)

		# draw the direction where the disk is going\
        # comment this on real application to minimize lag
		disk.draw_direction_line(img, (100, 100, 100))

		cv2.imshow("preview", img)

		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

	if not simulador:
		cv2.destroyAllWindows()