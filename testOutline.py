   #just a skeleton
   
   runTimeFile = open("userWalkTimes.txt", "a+")
   runTimeFile.write("user walk IP times\n")
   for i in range(1,100):
   start = time.clock()
   
   do some work
   
   end = time.clock()
   runTimeFile.write("%f\n" %(end-start))
   runTimeFile.close()
