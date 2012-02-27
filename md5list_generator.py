import md5
filehandle = open("filelist.txt")
md5fh = open("md5list.txt", "w")
for line in filehandle:
	fh = open(line.rstrip())
	m = md5.new()
	d = fh.read(8096) # saw this used online, not sure why 8096 exactly
	m.update(d)
	md5fh.write(m.hexdigest())
	fh.close()
filehandle.close()
md5fh.close()