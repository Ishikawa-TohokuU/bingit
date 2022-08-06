#!/bin/sh
exec ruby -S -x $0 "$@"

#! ruby

=begin
 A sturcure cutting program from a bulk  ver. 1.02
 Produced by Nobuki Ozawa   updated 2010/04/09 
=end

include Math
srand(11)
# readubg car file
print("Please input *.car file name\n")
#ifname=gets.chomp
ifname="zro2.car"
ofname="ysz.car"
ratio=8 #%

elem=["Zr","Y ","O"]
file1=open(ifname,"r")

i=0
num=0
index=""
coolist=Array.new

onum=0
znum=0
while line=file1.gets
  if i == 4 then
    data=line.split
    @xori=data[1].to_f*0.5
    @yori=data[2].to_f*0.5
    @zori=data[3].to_f*0.5
    index << line
  elsif i >= 5 then
    coolist[i-5]=line
    data=line.split
    onum+=1 if (data[7]==elem[2])
    znum+=1 if (data[7]==elem[0])
  else
    index << line
  end
  i+=1
end
total=i-7
file1.close

rnum=(znum*ratio.to_f/100.0).to_i
rnum+=1 if (znum*4-rnum)%2==1
#To make sure total charge equal to zero, ((znum-rum)*4 - 3*rnum)%2 == 0
onum2=(znum*4-rnum)/2
#onum = znum*2 - rnum/2
dnum=onum-onum2
#dnum=rnum/2
printf("%d %d %d %d\n",onum,znum,rnum,dnum)

fnum=0
while (fnum != rnum)
  fnum=0
  list1=""
  i=0
  while (i< total)
     line=coolist[i]
     data=line.split
     if (elem[0]==data[7])  then
        a=rand(100)
        if (a<9) then
#        printf("Zr %d %d %d\n",i,a,fnum)	
	 #str = "%s    %13.9f   %13.9f   %14.9f XXXX 1      xx     %s   0.000\n" %(elem[1], posx[i], posy[i], posz[i], AtomSymb[aSpec[i]-1]))
        list1<<line.gsub(elem[0],elem[1])
        fnum+=1
        else
        list1<<line
        end
     end
     i+=1
  end 
end

fnum=0
while (fnum != dnum)
  fnum=0
  list2=""
  i=0
  while (i< total)
     line=coolist[i]
     data=line.split
     if (elem[2]==data[7])  then
        a=rand(onum)
        if (a<dnum) then
#        printf("%d %d %d\n",i,a,fnum)
        fnum+=1
        else
        list2<<line
        end
     end
     i+=1
  end 
end


file2=open(ofname,"w")
file2.printf("%s",index)
file2.printf("%s",list1)
file2.printf("%s",list2)
file2.printf("end\n")
file2.printf("end\n")
file2.close
