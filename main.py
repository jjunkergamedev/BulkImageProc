# Bulk Image Tool: Processes bulk images using PIL

from PIL import Image
import glob
import os
import importlib
import utilities.images

def get_input_files(glob_pattern):
	files = glob.glob(glob_pattern)
	return [os.path.relpath(file) for file in files]

def get_output_files(output_directory, input_files, name_func):
	result = []

	output_index = 0
	prev_src_image = None
	for in_file in input_files:
		path, filename = os.path.split(in_file)
		name, ext = filename.split(".")

		if path:
			relpath = os.path.relpath(path)
		else:
			relpath = ".."

		out_path = output_directory.replace("<path>", relpath)
		out_name = name_func(filename, output_index)

		src_image = Image.open(in_file)
		if not utilities.images.are_images_equal(src_image, prev_src_image):
			result.append(os.path.join(out_path, out_name))
			prev_src_image = src_image
			output_index += 1

	print("output files: %s" % (result))

	# Make sure needed directories exist
	dirs_to_create = set()
	for out_file in result:
		out_dir = os.path.dirname(out_file)
		dirs_to_create.add(out_dir)

	for out_dir in dirs_to_create:
		if not os.path.exists(out_dir):
			print("making dir: %s" % (out_dir))
			os.makedirs(out_dir)

	return result

def run(in_glob_pattern, out_dir_pattern, mode_module):
	in_files = get_input_files(in_glob_pattern)
	print("input files: \n%s" % (in_files))

	out_files = get_output_files(out_dir_pattern, in_files, mode_module.name)
	print("output files: \n%s" % (out_files))

	out_index = 0
	prev_src_image = None
	for src_index, src_file in enumerate(in_files):
		src_image = Image.open(src_file)

		is_last = src_index == len(in_files) - 1
		out_image = mode_module.image(src_image)
		if out_image:
			dest_file = out_files[out_index]
			print("Saving %s" % (dest_file))
			out_image.save(dest_file)
			out_index += 1

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--src", help="The input files to process", default="*.*")
	parser.add_argument("--out", help="""The output directory. 

	Replacements:
	- <path>: The relative path to the input image.""", default="<path>/out")
	parser.add_argument("--mode", help="""The operation to apply to the source images.
Supported Operations:
- eternal_draft: crops and resizes screenshots from eternal""",default="eternal_draft")
	args = parser.parse_args()

	print("Mode", args.mode)

	mode_module_name = 'modes.{}'.format(args.mode)
	mode_module = importlib.import_module(mode_module_name)

	run(args.src, args.out, mode_module)

