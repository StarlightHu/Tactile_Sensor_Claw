import os

# SRC_PATH = "./fruit_data"
SRC_PATH = "./7_30"
TAR_PATH = "./fruit_data"

#SRC_PATH = "/Volumes/USB128/6_30"
#TAR_PATH = "/Volumes/USB128/6_30"

LABEL_PATH = "/Volumes/USB128/lab_data"

ls = []

count = 150

if __name__ == '__main__':
	for video in os.listdir(SRC_PATH):
		if os.path.exists(os.path.join(SRC_PATH, video, "info.txt")):
			fl = open(os.path.join(SRC_PATH, video, "info.txt"), "r")
			index_content = fl.readline()
			label_content = fl.readline()
			fl.close()
			last = index_content.split("\n")[0].split(":")[-1]
			print(video, end="")
			print(last)
			try:
				num = int(last)

				try:
					int(label_content.split("\n")[0].split(":")[-1])
				except:
					print("{}\nindex {} have an error '{}' label \n{}".format(
						'-' * 20,
						num,
						label_content.split("\n")[0].split(":")[-1],
						'-' * 20
					))
					raise ValueError

			except ValueError:
				continue

			if num > count or num == 0:
				continue

			ls.append(num)

			os.system("mv {} {}/".format(os.path.join(SRC_PATH, video), TAR_PATH))

	print("\nNot come numbers:")
	for i in range(1, count + 1):
		if i not in ls:
			print(i, end=",")
		if ls.count(i) > 1:
			print("more {}'s {}, ".format(ls.count(i), i))

	print("\nlen: ", len(os.listdir(TAR_PATH)))
