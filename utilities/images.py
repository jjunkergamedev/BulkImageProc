from PIL import ImageChops

def _scalar_to_fit(cur_width, cur_height, target_width, target_height):
	scale_x = target_width / cur_width
	scale_y = target_height / cur_height
	return min(scale_x, scale_y)

def scale_to_size(cur_width, cur_height, target_width, target_height):
	scalar = _scalar_to_fit(cur_width, cur_height, target_width, target_height)
	return (int(cur_width * scalar), int(cur_height * scalar))

def are_images_equal(img1, img2):
	result = False

	if img1 == img2:
		return True
	if img1 and img2:
		if img1.getdata() == img2.getdata():
			return True

		diff = ImageChops.difference(img1, img2)
		result = not diff.getbbox()

	return result