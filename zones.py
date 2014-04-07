import string
data_file_path = "../data/"

def createBeatsDoc():
  file = open(data_file_path + 'policezonebeat.txt','r')
# get the unique zones
  doc = file.read()
  all = doc.split()
  districts = []
  precinct = ""
  for a in all:
    if a[0:1] not in districts:
      districts.append(a[0:1])
    sorted_districts = sorted(districts)
#   create new file to use as lookup
    f = open(data_file_path + "police_districts.csv", "w")
#     header row
    f.write("district,precinct" + "\n")
    for d in sorted_districts:
      precinct = getPrecinct(d.lower())
      if d == "9":
        d = "99"
      f.write(d + "," + precinct + "\n")
#       print d
    f.close()
    file.close()

def getPrecinct(region):
  precinct = ""
  if region == "w" or region == "f":
    precinct = "Southwest"
  elif region == "o" or region == "r" or region == "s":
    precinct = "South"
  elif region == "d" or region == "k" or region == "m" or region == "q":
    precinct = "West"
  elif region == "e" or region == "c" or region == "g":
    precinct = "East"
  elif region == "b" or region == "j" or region == "l" or region == "n" or region == "u":
    precinct = "North"
  elif region == "9":
    precinct = "SR99"
  else:
    precinct = "na"
  return precinct

def main():
  createBeatsDoc()
#   print 'create lookup'
  
if __name__ == '__main__':
  main()