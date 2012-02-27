#with open('C:\\Documents and Settings\\pbooth\\My Documents\\classes\\fresh\\summer\\graph theory research\\graph program\\52.txt','r') as r5:
##num=1
##with open('C:\\Documents and Settings\\pbooth\\My Documents\\My Dropbox\\GPGlabelings\\boo.txt','r+') as boo:
##    num=int(boo.read())
##    boo.seek(0)
##    boo.write(str(num+1))

with open('C:\\My Dropbox\\GPGlabelings\\n10\\'+str(5)+'.txt','r') as r5:
    for line in r5:
        line=line.strip()
        nums=list(line)
        for i in xrange(len(nums)):
            nums[i]=int(nums[i])
        line=line+'.txt'
        f=open('C:\\Documents and Settings\\pbooth\\My Documents\\classes\\fresh\\summer\\graph theory research\\MT2GI-1.1.4\\precompiled\\nonisos\\'+line,'w')
        try:
            s='11-20,11-12,12-13,13-14,14-15,15-16,16-17,17-18,18-19,19-20,1-11,2-12,3-13,4-14,5-15,6-16,7-17,8-18,9-19,10-20,'
            for i in xrange(len(nums)-1):
                s=s+str(nums[i]+1)+'-'+str(nums[i+1]+1)+','
            s=s+str(nums[0]+1)+'-'+str(nums[-1]+1)
            f.write(s)
        finally:
            f.close()
