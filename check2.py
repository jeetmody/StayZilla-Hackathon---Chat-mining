import csv
import nltk
import re
import pickle
from datetime import date
from nltk.tokenize.punkt import PunktWordTokenizer
budget = []

with open('1234.csv') as csvfile:
     reader = csv.DictReader(csvfile)
 
   
     word=[]
     hb_count = []
     lb_count = []
     lb = ['inexpensive', 'cheap', 'cheaper', 'cheapest', 'low cost','low budget', 'budget', 'least cost', 'low price', 'low priced', 'low pricing', 'low amount','inexpensive', 'low costs', 'low costing', "lowest price"]
     hb = ['high budget', 'high price', 'high priced', 'high pricing', 'high costing', 'high costs', 'expensive', 'high amount']
     
     ac = ["ac ", "air-conditioned", "air conditioned", " a/c ", " a-c ", " AC ", " A.C .", " A/C "]
     nac = ["nac", "non ac", "non-ac", "non-airconditioned"]
     
     train = ["station", "train","railway"]
     bus = ["bus" , "bus stop" , "bus stand"]
     airport = ["flying", "plane","flight", "airport"] 
     source = ["from","currently at"]
     dest = ["going to", "arriving at", "to", "at"]
     people = ["number of", "number of people"]

     lb_cities = []
     hb_cities = []
     lb_dict = {}
     hb_dict = {}
     lb_final = {}
     hb_final = {}

     monthly = {1: {}, 2: {},3: {},4: {},5: {},6: {},7: {},8: {},9: {}, 10: {}, 11: {}, 12: {}, }

     avg2 = {}
     result = []
     for i in range(0,10):
         result.append([])
     times = 0
     for row in reader:
         print times
         times+=1
         #print "------new-row--------------------------------------"
         location = None
         
         
        #Message analysis code begins
         s = row['Chat Message']
         s=re.sub(r'[^\w]', ' ', s)
         #tokenized = PunktWordTokenizer().tokenize(s)

         #print s
         flag = 0
         #low / high budget
         
         for i in lb:
             if s.find(i) != -1:
                 result[0].append(1)
                 flag = 1
                 break
         if flag == 0:
             result[0].append(0)

         
             
                 
                 
         flag = 0    
         for i in hb:
            if s.find(i) != -1:
                result[1].append(1)
                flag = 1
                break
         if flag == 0:
             result[1].append(0)
            
         #ac / non ac
            
         flag = 0       
         for i in ac:
             if s.find(i) != -1 and (s[s.find(i) + 2] == " " or s[s.find(i) + 2] == "." or s[s.find(i) + 2] == ",")  :
                 result[2].append(1)
                 flag = 1
                 break
         if flag == 0:
             result[2].append(0)
                 
         flag = 0    
         for i in nac:
            if s.find(i) != -1:
                result[3].append(1)
                flag = 1
                break
         if flag == 0:
             result[3].append(0)

             
         flag = 0
         for i in train:
            if s.find(i) != -1:
                result[4].append(1)
                flag = 1
                break
         if flag == 0:
             result[4].append(0)

         flag = 0
                
         for i in bus:
            if s.find(i) != -1:
                result[5].append(1)
                flag = 1
                break
         if flag == 0:
             result[5].append(0)

         flag = 0
         for i in airport:
            if s.find(i) != -1:
                result[6].append(1)
                flag = 1
                break
         if flag == 0:
             result[6].append(0)
         
         flag = 0
         for i in source:
            if s.find(i) != -1:
                result[7].append(1)
                flag = 1
                break
         if flag == 0:            
             result[7].append(0)

         
         flag = 0       
         for i in dest:
            if s.find(i) != -1:
                result[8].append(1)
                flag = 1
                break
         if flag == 0:
             result[8].append(0)

         flag = 0
         for i in people:
            if s.find(i) != -1:
                result[9].append(1)
                flag = 1
                break
         if flag == 0:
             result[9].append(0)

         
             
         #for i in result:
          #   print i


         # date - location code begins
         
         t = row["h"]
        
         id = c_out = c_in = ""
         if t[0] in str(range(0,9)):
             c_count = 0
             
             for j in t:
                # print j, type(j),
                 if j == ":":
                     c_count+=1
                 elif c_count == 0:
                 #    print "id"
                     id = id + j
                 elif c_count == 1:
                
                     c_in = c_in + j
                 elif c_count == 2:
                   #  print "in"
                     c_out = c_out + j
             #c_out = t[len(t) - 10: len(t)]
             c_out = c_out.split("/")
             #c_in = t[len(t) - 21 :len(t) -11]
             c_in = c_in.split("/")
             #print "c_out", c_out
             c_out = [int(x) for x in c_out]
             c_in = [int(x) for x in c_in]
             #print c_out, c_in, "time"

             d_out = date(c_out[2], c_out[1], c_out[0])
             d_in = date(c_in[2], c_in[1], c_in[0])
             nod = d_out - d_in #no. of days
             days = abs(nod.days)
             
            # print "nod", nod.days

             
            
             id = ""
             i = 0
             #print type(t), ":t"
             
             while t[i] != ":":
                 id = id + t[i]
                 i+=1
                
             id = int(id)
             
                 
             with open('chat_location_mapping.csv') as csvfile2:
                 reader2 = csv.DictReader(csvfile2)

                 for row in reader2:
        
        
                     
                     if int(row["ID"]) == id:
                         location =  row["L"]
                         break
             #2
            
             if location:
                 if location not in monthly[c_in[1]].keys():
                     monthly[c_in[1]][location] = 1
                 else:
                     monthly[c_in[1]][location]+=1
             #3
            
             
             if location:
                 if location in avg2.keys():
                     avg2[location].append(days)
                     
                     
                     
                 else:
                     avg2[location] = [days]
                     
                     
                   
             
                     
             
                 
         #1               
             #print result[1][-1], "hb values", location, "location"
             if result[0][-1] == 1 and location:
                 lb_cities.append(location)
             else:
                 hb_cities.append(location)
         

             #if result[1][-1] == 1 and location:
                 #hb_cities.append(location)

             for i in lb_cities:
                 if i not in lb_dict.keys():
                     lb_dict[i] = lb_cities.count(i)
                
             for i in hb_cities:
                 if i not in hb_dict.keys():
                     hb_dict[i] = hb_cities.count(i)

             for i in lb_dict.keys():
                 if i in hb_dict.keys():
                     lb_final[i] = (lb_dict[i]/(lb_dict[i] + hb_dict[i])) * 100
                     hb_final[i] = 100 - lb_final[i]
                 else:
                     lb_final[i] = 100
                     hb_final[i] = 0

             for i in hb_dict.keys():
                 if i in lb_dict.keys():
                     hb_final[i] = (hb_dict[i]/(hb_dict[i] + lb_dict[i])) * 100
                     lb_final[i] = 100 - hb_final[i]
                 else:
                     hb_final[i] = 100
                     lb_final[i] = 0 
                 
print lb_final, "lb\n", hb_final, "hb"
#print monthly,
for i in avg2.keys():
    avg2[i] = sum(avg2[i])/len(avg2[i])
    
print avg2

with open('my_data.csv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    for key in avg2.keys():
        f.write(str(key) + ":" + str(avg2[key]) + ",");



print monthly

                                      




            
        
    



        


            




         
         




        
                 
                 
                 
         

    
        
         
