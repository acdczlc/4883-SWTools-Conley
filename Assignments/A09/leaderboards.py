import csv

score=input("Please enter your score: ")
username=input("Please enter your name: ")

with open ("protleader.csv", "a", newline='') as file:
    fields=['score', 'name']
    writer=csv.DictWriter(file, fieldnames=fields)
    writer.writerow({'score' : score, 'name' : username})

with open ("protleader.csv", "r") as file:
    sortlist=[]
    reader=csv.reader(file)
    for i in reader:
        sortlist.append(i)
for i in range(len(sortlist)):
    if i != 0:
        sortlist[i][0]=int(sortlist[i][int(0)])


print("")

print("Unsorted:")
for i in range(len(sortlist)):
    print(sortlist[i])


for i in range(555):
    for i in range(len(sortlist)-1):
        if i != 0:
            if sortlist[i][0] < sortlist[i+1][0]:
                change=sortlist[i]
                sortlist[i]=sortlist[i+1]
                sortlist[i+1]=change


print("")

print("Sorted and cut:")
for i in range(len(sortlist)-1):
    print(sortlist[i])