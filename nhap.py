import csv
board=[]
with open('input1.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        intRow = [int(element) for element in row]
        board += [intRow]
print(board)