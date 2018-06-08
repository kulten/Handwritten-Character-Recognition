import csv
text = "asdf"
csvfile = "tocsv.csv"
newcsvfile = text+".csv"


#create temp csv file for student - tocsv.csv
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow("flattened image goes here")

#write rows of tocsv to studentname.csv with student name as label followed by image
with open(csvfile,'r') as csvinput:
    with open(newcsvfile, 'a') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        for row in csv.reader(csvinput):
            writer.writerow([text]+row)
