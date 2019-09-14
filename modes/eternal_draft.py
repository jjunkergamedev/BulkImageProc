# Processes images from Eternal Card Game
import utilities.images

def name(source_name, index):
	return '{:0>2}_p{:d}p{:d}.jpg'.format(index + 1, int(index / 12) + 1, index % 12 + 1)

def image(src_image):
	aspect_ratio = float(src_image.width) / float(src_image.height)
	if aspect_ratio == 3840.0 / 2160.0:
		rel_box = (0.193, 0.058, 3300.0 / 3840.0, 0.926)
	else:
		print("unsupported aspect ratio %s" % (aspect_ratio))
		return None

	src_box = (src_image.width, src_image.height, src_image.width, src_image.height)
	actual_box = [int(rel_val * size_val) for rel_val, size_val in zip(rel_box, src_box)]

	print("src_box:", src_box, "actual_box:", actual_box)

	result = src_image.crop(box=actual_box)

	print("result width:", result.width, "result height: ", result.height)

	target_size = 1200
	if result.width > target_size or result.height > target_size:
		result = result.resize(utilities.images.scale_to_size(result.width, result.height, 800, 800))

	return result
