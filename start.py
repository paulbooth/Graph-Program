import urllib
from shutil import move
SERVER = "http://paulbooth.github.com/Graph-Program/"

#TODO: keep website in separate file, so it can be updated.  Maybe provide mechanism to update auto-update script?

#go through old filelist, find the line number of filename
#return None if it doesn't exits
#otherwise, return corresponding md5sum
def getoldmd5(filename):
    oldlist = open("filelist.old")
    i = 0
    found = 0
    for line in oldlist:
        if line.rstrip() == filename:
            found = 1
            break
        else:
            i = i + 1
    oldlist.close()
    if not found:
        return None
    
    # It is found; return corresponding md5
    oldlist = open("md5list.old")
    oldlist.read(16*i)
    oldmd5 = oldlist.read(16)
    oldlist.close()
    return oldmd5
    
def srv_path(path):
    a = path.split("/")
    return a[-1]

def check_for_updates():
    print "Checking for updates..."
    
    try:
        filehandle = urllib.urlopen(SERVER + "rev")
    except: # Identify error here?  Just a "can't connect error; afraid it might be different in different cases.
        print "Unable to connect to the internet!"
        return 'NO_CONNECTION'
    
    remote_rev = filehandle.read()
    filehandle.close()
    
    try:
        remote_rev = int(remote_rev)
    except:
        print "Error in server revision file! Notify developer!"
        return 'BAD_SVR_FILE'
        
    try:
        filehandle = open("rev")
        local_rev = filehandle.read()
    except:
        print "No revision file found in installation. Installing program"
        local_rev = 0
        filehandle = open("rev","w")
        filehandle.write("0")
        filehandle.close()
        from os import mkdir
        mkdir("icons")
        mkdir("icons/subgraphs")
        filehandle = open("filelist.txt","w")
        filehandle.write("")
        filehandle.close()
        filehandle = open("md5list.txt","w")
        filehandle.write("")
        
    filehandle.close()
    
    try:
        local_rev = int(local_rev)
    except:
        print "Error in local revision file. Please reinstall."
        return 'BAD_LOC_FILE'
    
    if remote_rev > local_rev:
        print "Update found: please wait while updates are downloaded..."
        move("filelist.txt", "filelist.old")
        move("md5list.txt", "md5list.old")
        urllib.urlretrieve(SERVER + "filelist.txt","filelist.txt")
        urllib.urlretrieve(SERVER + "md5list.txt","md5list.txt")
        filelist = open("filelist.txt")
        md5list = open("md5list.txt")
        for file in filelist.readlines():
            file = file.rstrip()
            md5 = md5list.read(16)
            oldmd5 = getoldmd5(file)
            if md5 != oldmd5:
                print "downloading newer version of " + file + "."
                urllib.urlretrieve(SERVER + srv_path(file),file)
            else:
                print file + " is unchanged."
        filelist.close()
        md5list.close()
        move("rev", "rev.old") #Backup in case anything changes
        urllib.urlretrieve(SERVER + "rev","rev")
        urllib.urlretrieve(SERVER + "start.py","start.py.new")
        #TODO: What's new message?
        return 'UPDATED'
    elif remote_rev == local_rev:
        print "You are running the latest version."
        return 'CURRENT'
    else:
        print "Local revision is higher than server revision!!!"
        print "Development mode:"
        urllib.urlretrieve(SERVER + "filelist.txt","filelist.old")
        urllib.urlretrieve(SERVER + "md5list.txt","md5list.old")
        filelist = open("filelist.txt")
        md5list = open("md5list.txt")
        for file in filelist.readlines():
            file = file.rstrip()
            md5 = md5list.read(16)
            oldmd5 = getoldmd5(file)
            if md5 != oldmd5:
                print file + " has changed"
        print "Finished checking files."
        filelist.close()
        md5list.close()
        
        
        return 'LOC_GT_SVR'

        
res = check_for_updates()
if res in ['CURRENT','NO_CONNECTION','BAD_SVR_FILE']:
    print "Starting Graph Program"
    try:
        import graphgui
    except:
        print "you must be connected to the internet for installation!"
        exit(-1)
    graphgui.main()
elif res == 'UPDATED':
    print "Starting Graph Program"
    import graphgui
    graphgui.main(update = True)
else:
    print "Please correct errors!!!"
    print "Starting Graph Program Anyway..."
    import graphgui
    graphgui.main()
   
    