# Henry Frye, Spring AY24

import csv

# dictionaries for each class
first = {}
second = {}
third = {}
fourth = {}
coSEL = {}
itemDict = {}

fname = input("Enter the input .csv file name: ")
ofname = input("Enter the output .csv file name: ")
totalCost = 0

with open(fname, "r") as csvfile:
    reader = csv.reader(csvfile)
    header = []

    # retrieve sheet header
    for row in reader:
        header = row
        break

    priceList = []

    # organize items and prices into dict
    for i in range(7, len(header)):
        try:
            fullItem = header[i].split("[")[1].strip("]")
            name = fullItem.split("(")[0].strip()
            price = float(fullItem.rsplit("(")[1].strip(")"))
            priceList.append(price)
            itemDict[name] = price
        except:
            print("ERROR", header[i])

    itemsList = list(itemDict.values())

    # iterate through rest of rows
    # row[1] == class
    for row in reader:
        # skip header row
        if "Timestamp" in row:
            continue

        # get class year
        year = row[1]

        # figure out what they ordered
        itemOrder = row[7:]

        total = 0

        for i in range(0, len(itemOrder)):
            if itemOrder[i]:
                try:
                    total += (float(itemOrder[i]) * priceList[i])
                    totalCost += (float(itemOrder[i]) * priceList[i])
                except:
                    print(row)
                    print(itemOrder)

        # store data
        if year == "1/C":
            name = row[2].strip()
            if name in first:
                first[name] += total
            else:
                first[name] = total
        elif year == "2/C":
            name = row[3].strip()
            if name in second:
                second[name] += total
            else:
                second[name] = total
        elif year == "3/C":
            name = row[4].strip()
            if name in third:
                third[name] += total
            else:
                third[name] = total
        elif year == "4/C":
            name = row[5].strip()
            if name in fourth:
                fourth[name] += total
            else:
                fourth[name] = total
        elif year == "CO/SEL":
            name = row[6].strip()
            if name in coSEL:
                coSEL[name] += total
            else:
                coSEL[name] = total

# sort dictionaries
firstKeys = list(first.keys())
firstKeys.sort()
firstSorted = {i: first[i] for i in firstKeys}

secondKeys = list(second.keys())
secondKeys.sort()
secondSorted = {i: second[i] for i in secondKeys}

thirdKeys = list(third.keys())
thirdKeys.sort()
thirdSorted = {i: third[i] for i in thirdKeys}

fourthKeys = list(fourth.keys())
fourthKeys.sort()
fourthSorted = {i: fourth[i] for i in fourthKeys}

coSELKeys = list(coSEL.keys())
coSELKeys.sort()
coSELSorted = {i: coSEL[i] for i in coSELKeys}

print("---1/C---")
for pair in firstSorted.items():
    print(f"{pair[0]}: ${pair[1]}")
print("---2/C---")
for pair in secondSorted.items():
    print(f"{pair[0]}: ${pair[1]}")
print("---3/C---")
for pair in thirdSorted.items():
    print(f"{pair[0]}: ${pair[1]}")
print("---4/C---")
for pair in fourthSorted.items():
    print(f"{pair[0]}: ${pair[1]}")
print("---CO/SEL---")
for pair in coSELSorted.items():
    print(f"{pair[0]}: ${pair[1]}")
print(f"Total Wardroom Store Bill Cost: {totalCost}")

# write results out to new csv
with open(ofname, 'w') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in firstSorted.items():
        writer.writerow([key, value])
    for key, value in secondSorted.items():
        writer.writerow([key, value])
    for key, value in thirdSorted.items():
        writer.writerow([key, value])
    for key, value in fourthSorted.items():
        writer.writerow([key, value])
    for key, value in coSELSorted.items():
        writer.writerow([key, value])