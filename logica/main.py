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
			img = np.array(pyautogui.screenshot(region=(1200, 200, 500, 750)))
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		else:
			ret, img = cap.read()

		mask = disk_mask(img, disk_lower, disk_upper)

		center = get_disk_center(mask, img)
		if center != None:
			disk.new_pos(center)

		disk.draw_direction_line(img, (100, 100, 100))

		# drawing map important things
		draw_horizontal_line(img, defense_line_y, (250, 0, 255))
		draw_vertical_line(img, lateral_line0_x, (250, 0, 255))
		draw_vertical_line(img, lateral_line1_x, (250, 0, 255))
		
		p = disk.intersections(img, (255, 255, 255), (0, 170, 255), lateral_line0_x, lateral_line1_x, defense_line_y, 900, 4)
		print(p)

		cv2.imshow("preview", img)

		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

if not simulador:
	cv2.destroyAllWindows()