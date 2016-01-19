import sys

def hashing_func(tablesize,string_to_hash):
    sum = 0
    for i in string_to_hash:
        sum+=ord(i)
    hash_value=sum%tablesize
    return(hash_value)

def getWords(words_file):
    word_count_map = {}
    with open(words_file, 'r') as f:
        for line in f.readlines():
            for word in line.strip().split(","):
                if word in word_count_map:
                    word_count_map[word] += 1
                else:
                    word_count_map[word] = 1
    return word_count_map

def Singles():
   min_support=int(sys.argv[2])
   inputdata = open(sys.argv[1])
   SingleWords=[]
   no_of_buckets=int(sys.argv[3])
   bitmap=[]*no_of_buckets  
   bucket_count=[0]*no_of_buckets
   wordsDict = getWords(sys.argv[1])
   for keys in sorted(wordsDict.keys()):
     if wordsDict[keys]>=min_support:
       SingleWords.append(keys)
   if SingleWords:
     print ("Frequent Itemsets of size 1")
     for word in sorted(SingleWords):
        print (word)
   print("\n")


   inputdata = open(sys.argv[1])
   for line in inputdata:
     itemsperline=[]
     for words in line.strip().split(","):
         itemsperline.append(words)  
     
     for i in range(0,len(itemsperline)-1):
        for j in range(0,len(itemsperline)):
             hash_val=hashing_func(no_of_buckets,(itemsperline[i]+itemsperline[j]))
             bucket_count[hash_val]+=1
   for value in bucket_count:
       if value<min_support:
          bitmap.append(0)
       else:
          bitmap.append(1)
   return (SingleWords,bitmap)

def Pairs(SingleWords,bitmap):
   min_support=int(sys.argv[2])
   inputdata = open(sys.argv[1])
   no_of_buckets=int(sys.argv[3])
   pairing = []
   
   for line in inputdata:
     itemsperline=[]
     for words in line.strip().split(","):
         itemsperline.append(words)  
     
     for i in range(0,len(itemsperline)-1):
        for j in range(0,len(itemsperline)):
             hash_val=hashing_func(no_of_buckets,(itemsperline[i]+itemsperline[j]))
             if bitmap[hash_val]==1:
                    if itemsperline[i] in SingleWords and itemsperline[j] in SingleWords:
                         if itemsperline[j]>itemsperline[i]:
                               pairing.append((itemsperline[i],itemsperline[j]))
                         else :
                               pairing.append((itemsperline[i],itemsperline[i]))
   norepeat = []
   [norepeat.append(item) for item in pairing if item not in norepeat]
   word_count_dict={}
   inputdata = open(sys.argv[1])
   for line in inputdata:
    for word in norepeat:
     if word[0] in line and word[1] in line:
         if word[0]<word[1]:
            tuple1=(word[0],word[1])
            word_count_dict[tuple1] = word_count_dict.get(tuple1, 0) + 1
         elif word[0]>word[1]:
            tuple1=(word[1],word[0])
            word_count_dict[tuple1] = word_count_dict.get(tuple1, 0) + 1
   FreqPairs=[]
   for tuple1 in word_count_dict:
     if word_count_dict[tuple1]>=min_support:
       FreqPairs.append((tuple1[0]+","+tuple1[1]))
   if FreqPairs:
     print ("Frequent Itemsets of size 2")
     for item in sorted(FreqPairs):
       print(item)
   return FreqPairs

def Gen_pcy(type_of_data,SingleWords,IncreasingList):
   min_support=int(sys.argv[2])
   print("\n")
   large_data_list=[]   
   Resultant_List=[]
   for w1 in SingleWords:
      for w2 in IncreasingList:
         if w1 not in w2:
           holder=[]
           holder.append((w1+","+w2))
           large_data_list.append(sorted(holder[0].split(",")))
   for bucket_item in large_data_list:
      indicator=1;
      for index in range (0,len(bucket_item)):
         pos=0
         str=""
         while pos<len(bucket_item):
           if pos!=index:
              if str=="":
                str+=(bucket_item[pos])
              else:
                str+=","+(bucket_item[pos])
           pos=pos+1
         if str not in IncreasingList:
                indicator=-1;
      if indicator==1: 
          str=""
          inputdata = open(sys.argv[1])
          keep_counting=0;
          
          candidate_set=set()
          for item in bucket_item:
             if str=="":
                  str+=item
                  candidate_set.add(item)
             else:
                  str+=","+item
                  candidate_set.add(item)
          for basket in inputdata:
             basket=basket.strip('\n')
             basket=basket.split(",")
             item_holder=set()
             for item in sorted(basket):
               item_holder.add(item)
             if candidate_set.issubset(item_holder):
                keep_counting=keep_counting+1;
          if keep_counting>=min_support:
             Resultant_List.append(bucket_item)
   Final=[]
   for items in Resultant_List:
      string1=""
      for item in items:
       if string1=="":
        string1=string1+item
       else:
        string1=string1+","+item
      Final.append(string1)
   norepeat = []
   [norepeat.append(items) for items in Final if items not in norepeat]
   if norepeat:
     str="Frequent Itemsets of size "
     str+=format(type_of_data)
     print (str)
     for data in norepeat:
       print(data)
   return norepeat

if __name__ == '__main__':
  type_of_data=1
  SingleWords,bitmap=Singles()
  if SingleWords:
   type_of_data+=1
   IncreasingList=Pairs(SingleWords,bitmap)
  type_of_data+=1
  while IncreasingList:
    Received_Data=[]
    Received_Data=Gen_pcy(type_of_data,SingleWords,IncreasingList)
    IncreasingList=Received_Data
    type_of_data+=1    
