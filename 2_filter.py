import os

SRC_PATH = "./fruit_data"
#SRC_PATH = "./3_50"
TAR_PATH = "./3_50"

ls = []



if __name__ == '__main__':
	for video in os.listdir(SRC_PATH):
		if os.path.exists(os.path.join(SRC_PATH, video, "info.txt")):
			fl = open(os.path.join(SRC_PATH, video, "info.txt"), "r")
			content = fl.readline()
			fl.close()
			last = content.split("\n")[0].split(":")[-1]
			print(video, end="")
			print(last)
			try:
				num = int(last)
			except ValueError:
				continue
				
			ls.append(num)
			
			
			if num > 100 or num == 0:
				continue
				
			os.system("mv {} {}/".format(os.path.join(SRC_PATH, video), TAR_PATH))
	
	print("\nNot come numbers:")			
	for i in range(1, 101):
		if i not in ls:
			print(i, end="")
			
	print("\nlen: ", len(os.listdir(TAR_PATH)))
			
	
			
		
