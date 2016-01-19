import sys

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
   wordsDict = getWords(sys.argv[1])
   for keys in sorted(wordsDict.keys()):
     if wordsDict[keys]>=min_support:
       SingleWords.append(keys)
   if SingleWords:
     print ("Frequent Itemsets of size 1")
     for word in sorted(SingleWords):
        print (word)
   print("\n")
   return SingleWords

def Pairs(SingleWords):
   min_support=int(sys.argv[2])
   inputdata = open(sys.argv[1])
   pairing = []
   for i in range(0,len(SingleWords)-1):
     for j in range(i+1,len(SingleWords)):
       if SingleWords[j]>SingleWords[i]:
           pairing.append((SingleWords[i],SingleWords[j]))
       else :
           pairing.append((SingleWords[j],SingleWords[i]))
   word_count_dict={}
   for line in inputdata:
    for word in pairing:
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

def Gen_apriori(type_of_data,SingleWords,IncreasingList):
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
          inputdata = open(sys.argv[1])
          keep_counting=0;
          str=""
          candidate_set=set()
          for item in bucket_item:
             if str=="":
                  str+=item
                  candidate_set.add(item)
             else:
                  str+=","+item
                  candidate_set.add(item)
          for bucket in inputdata:
             bucket=bucket.strip('\n')
             bucket=bucket.split(",")
             item_holder=set()
             for item in sorted(bucket):
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
  SingleWords=Singles()
  if SingleWords:
   type_of_data+=1
   IncreasingList=Pairs(SingleWords)
  type_of_data+=1
  while IncreasingList:
    Received_Data=[]
    Received_Data=Gen_apriori(type_of_data,SingleWords,IncreasingList)
    IncreasingList=Received_Data
    type_of_data+=1    
