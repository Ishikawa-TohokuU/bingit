#!/bin/sh
exec ruby -S -x $0 "$@"

#! ruby

=begin
 A sturcure cutting program from a bulk  ver. 1.02
 Produced by Nobuki Ozawa   updated 2010/04/09 
=end

include Math

# readubg car file
print("Please input *.car file name\n")
ifname=gets.chomp

file1=open(ifname,"r")

i=0
num=0
index=""
coolist=Array.new
ofname="newcut.car"

while line=file1.gets
if i == 4 then
  data=line.split
  @xori=data[1].to_f*0.5
  @yori=data[2].to_f*0.5
  @zori=data[3].to_f*0.5
  index << line
  elsif i >= 5 then
   coolist[i-5]=line
  else
    index << line
  end
  i+=1
  end
  tnum=i-7
file1.close

# select cutting mode
print("Please choice cutting mode\n")
print("cube [c], sphere [s], dodecahedron [12], fourteen-faced [14], octadecahedron [18]\n")
strname=gets.chomp

def cube(list,num)
 print("Please input cutoff value\n")
 cutoff=gets.to_f
 flag=6

 i=0
 j=0
 out=""
 while i < num
  cont=0
  line=list[i]
  data=line.split
  x=data[1].to_f-@xori
  y=data[2].to_f-@yori
  z=data[3].to_f-@zori

  cont+=1 if x-cutoff/2 <= 0
  cont+=1 if y-cutoff/2 <= 0
  cont+=1 if z-cutoff/2 <= 0
  cont+=1 if -x-cutoff/2 <= 0
  cont+=1 if -y-cutoff/2 <= 0
  cont+=1 if -z-cutoff/2 <= 0

  out << line if cont==flag
  j+=1 if cont==flag
  i+=1
 end
 return out, j
end

def sphere(list,num)
 print("Please input cutoff value\n")
 cutoff=gets.to_f
 flag=1

 i=0
 j=0
 out=""
 while i < num
  cont=0
  line=list[i]
  data=line.split
  x=data[1].to_f-@xori
  y=data[2].to_f-@yori
  z=data[3].to_f-@zori

  cont+=1 if x*x+y*y+z*z-cutoff*cutoff <= 0

  out << line if cont==flag
  j+=1 if cont==flag
  i+=1
 end
 return out, j
end

def fourteen(list,num)
 print("Please input cutoff value\n")
 cutoff=gets.to_f
 flag=14

 i=0
 j=0
 out=""
 while i < num
  cont=0
  line=list[i]
  data=line.split
  x=data[1].to_f-@xori
  y=data[2].to_f-@yori
  z=data[3].to_f-@zori

  cont+=1 if x-sqrt(2)*cutoff <= 0
  cont+=1 if y-sqrt(2)*cutoff <= 0
  cont+=1 if z-sqrt(2)*cutoff <= 0
  cont+=1 if -x-sqrt(2)*cutoff <= 0
  cont+=1 if -y-sqrt(2)*cutoff <= 0
  cont+=1 if -z-sqrt(2)*cutoff <= 0
  cont+=1 if x+y+z-sqrt(4.5)*cutoff <= 0
  cont+=1 if x-y+z-sqrt(4.5)*cutoff <= 0
  cont+=1 if x+y-z-sqrt(4.5)*cutoff <= 0
  cont+=1 if x-y-z-sqrt(4.5)*cutoff <= 0
  cont+=1 if -x+y+z-sqrt(4.5)*cutoff <= 0
  cont+=1 if -x-y+z-sqrt(4.5)*cutoff <= 0
  cont+=1 if -x+y-z-sqrt(4.5)*cutoff <= 0
  cont+=1 if -x-y-z-sqrt(4.5)*cutoff <= 0

  out << line if cont==flag
  j+=1 if cont==flag
  i+=1
 end
 return out, j
end

def octadecahedron (list,num)
 print("Please input cutoff value\n")
 cutoff=gets.to_f
 flag=18

 i=0
 j=0
 out=""
 while i < num
  cont=0
  line=list[i]
  data=line.split
  x=data[1].to_f-@xori
  y=data[2].to_f-@yori
  z=data[3].to_f-@zori
  
  ratio=1.2*cutoff
  cont+=1 if x+y-ratio <= 0
  cont+=1 if x-y-ratio <= 0
  cont+=1 if -x+y-ratio <= 0
  cont+=1 if -x-y-ratio <= 0
  cont+=1 if y+z-ratio <= 0
  cont+=1 if y-z-ratio <= 0
  cont+=1 if -y+z-ratio <= 0
  cont+=1 if -y-z-ratio <= 0
  cont+=1 if z+x-ratio <= 0
  cont+=1 if z-x-ratio <= 0
  cont+=1 if -z+x-ratio <= 0
  cont+=1 if -z-x-ratio <= 0

  ratio=0.9*cutoff
  cont+=1 if x-ratio <= 0
  cont+=1 if y-ratio <= 0
  cont+=1 if z-ratio <= 0
  cont+=1 if -x-ratio <= 0
  cont+=1 if -y-ratio <= 0
  cont+=1 if -z-ratio <= 0
 
  out << line if cont==flag
  j+=1 if cont==flag
  i+=1
 end
 return out, j
end

def dodecahedron (list,num)
 print("Please input cutoff value\n")
 cutoff=gets.to_f
 flag=12

 i=0
 j=0
 out=""
 while i < num
  cont=0
  line=list[i]
  data=line.split
  x=data[1].to_f-@xori
  y=data[2].to_f-@yori
  z=data[3].to_f-@zori
  ratio=1.2*cutoff

  cont+=1 if x+y-ratio <= 0
  cont+=1 if x-y-ratio <= 0
  cont+=1 if -x+y-ratio <= 0
  cont+=1 if -x-y-ratio <= 0
  cont+=1 if y+z-ratio <= 0
  cont+=1 if y-z-ratio <= 0
  cont+=1 if -y+z-ratio <= 0
  cont+=1 if -y-z-ratio <= 0
  cont+=1 if z+x-ratio <= 0
  cont+=1 if z-x-ratio <= 0
  cont+=1 if -z+x-ratio <= 0
  cont+=1 if -z-x-ratio <= 0
 
  out << line if cont==flag
  j+=1 if cont==flag
  i+=1
 end
 return out, j
end

if strname=="c" then
 outlist, cnum=cube(coolist,tnum)
elsif strname=="s" then
 outlist, cnum=sphere(coolist,tnum)
elsif strname=="12" then
 outlist, cnum=dodecahedron(coolist,tnum)
elsif strname=="14" then
 outlist, cnum=fourteen(coolist,tnum)
elsif strname=="18" then
 outlist, cnum=octadecahedron(coolist,tnum)
else
 print("This cutting mode is not available!\n")
 exit
end

printf("Total number of atoms %s\n",cnum	)

file2=open(ofname,"w")
file2.printf("%s",index)
file2.printf("%s",outlist)
file2.printf("end\n")
file2.printf("end\n")
file2.close
