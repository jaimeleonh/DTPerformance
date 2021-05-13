def lookForPU ( fileToUse, default=200 ):
  fileToUse = fileToUse.lower()
  a = fileToUse.find("pu")
  print fileToUse,a
  if a == -1 :
    print("First Error: PU not found in file's name")
    return default

  if (a > 1 and  fileToUse[a-1] == "o" and  fileToUse[a-2] == "n" ) :
    return 0

  elif (a > 1 and ord(fileToUse[a-1]) >= 48 and ord(fileToUse[a-1])<=57) :
    num = 0
    exp = 1 
    while ( ord(fileToUse[a-1]) >= 48 and ord(fileToUse[a-1])<=57) :
      num += exp*int (fileToUse[a-1]);
      exp *= 10
      a-=1
    return num

  elif ( ord(fileToUse[a+2]) >= 48 and ord(fileToUse[a+2])<=57) :
    num = 0
    exp = 1
    tot = 0 
    while ( ord(fileToUse[a+2+tot]) >= 48 and ord(fileToUse[a+2+tot])<=57) :
      tot+=1
      if a+2+tot == len(fileToUse) : break

    for i in range (0, tot) :
      num += exp*int (fileToUse[a+2+tot-i-1]);
      exp *= 10
    return num

  else : 
    print("Error: PU not found in file's name")
    return default

