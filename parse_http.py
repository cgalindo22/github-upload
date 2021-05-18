#!/usr/bin/python3.5
# LAB 13_14 PARSING
import re
import argparse

rqstrs = {}
resours = {}
hourDate = {}
dateDict = {}
sortedReq = {}
sortedReso = {}
sortedHr = {}
resourceWords = ''
hourlyW = '' 
wholeDate = ''
topNum = ''
low = ''
high = ''

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

# the following are optional arguements inless required=True is set
parser.add_argument("-num", "--number", help="indicates the number of top lines", nargs=1, type=int)
parser.add_argument("-d", "--day", help="Defines the day, or range of days to be parsed. The format is --day 12 | --day 12-18", nargs=1, type=str, required=True)

# the following are mutually exclusive arguments (i.e. only one from the list can be applied) 
group.add_argument("-r", "--resources", help=" Displays a lost if the resources requested and the number of times they were requested, sorted from most to least reequested.", action="store_true")
group.add_argument("-req", "--requesters", help="Dsiplays a list of the host/IP addresses that requested resouces and the number of request made, sorted from most to least.", action="store_true" )
group.add_argument("-e", "--errors", help="Displays the number of times a resource was requested and the request returned an error sorted from most to least.", action="store_true")
group.add_argument("-hr", "--hourly", help="Counts the number of requests received, sorts and then displays them by the hour in which the request was received.", action="store_true")

# positional argument does not begin with a hyphen
parser.add_argument("file", help="Required. Enter file path to be parsed.", type=str)

args = parser.parse_args()
# print('Here is the output of args')
# print(args)
print("\n")
http_log = open(args.file, encoding="ISO-8859-1")

## FOR LOOP TO CREATE THE DICTIONARIES ##
for line in http_log:
  line = line.strip()
  words = line.split(" ")
  ## get --day from args and log file ##
  day = words[3][:2] # day from log file
  dayStr = args.day[0] # day from CL
  lenStr = len(dayStr) 
  ## REQUESTERS ##
  if args.requesters:
    if dayStr in day:
      if words[0] in rqstrs:
        rqstrs[words[0]] += 1
      else:
        rqstrs[words[0]] = 1
    elif '-' in dayStr:
      low = dayStr[:2]
      high = dayStr[3:5]
      if low <=  day and high >= day:
        if words[0] in rqstrs:
          rqstrs[words[0]] += 1
        else:
          rqstrs[words[0]] = 1
  ## RESOURCES ##
  elif args.resources:
    resourceWords = line.split('"')[1]
    if dayStr in day:
      if resourceWords in resours:
        resours[resourceWords] += 1
      else:
        resours[resourceWords] = 1
    elif '-' in dayStr:
      low = dayStr[:2]
      high = dayStr[3:5]
      if low <=  day and high >= day:
        if resourceWords in resours:
          resours[resourceWords] += 1
        else:
          resours[resourceWords] = 1
  ## ERRORS ##
  elif args.errors: 
    errorW = words[7]
    resourceWords = line.split('"')[1]
    if dayStr in day:
      if errorW == '400' or errorW == '500':
        if resourceWords in resours:
          resours[resourceWords] += 1
        else:
          resours[resourceWords] = 1
    elif '-' in dayStr:
      low = dayStr[:2]
      high = dayStr[3:5]
      if errorW == '400' or errorW == '500':
        if low <=  day and high >= day:
          if resourceWords in resours:
            resours[resourceWords] += 1
          else:
            resours[resourceWords] = 1
  ## HOURLY ##
  elif args.hourly: 
    ## --hourly ##
    wholeDate = words[3] 
    if dayStr in day:
      if wholeDate in dateDict:
        dateDict[wholeDate] += 1
      else:
        dateDict[wholeDate] = 1
    elif '-' in dayStr:
      low = dayStr[:2]
      high = dayStr[3:5]
      if low <=  day and high >= day:
        if wholeDate in dateDict:
          dateDict[wholeDate] += 1
        else:
          dateDict[wholeDate] = 1

### PRINT REQUESTERS with TOP NUM ##
if args.requesters and args.number: ## handle top number
  topNum = args.number[0]
  top = int(topNum)
  sortedReq = dict(sorted(rqstrs.items(), key=lambda x: x[1], reverse=True))
  if len(sortedReq) > topNum:
    for i in range(top):
      print(list(sortedReq.keys())[i], "\t", list(sortedReq.values())[i])
  else:
    print("\nError: Number needs to be smaller.\n")
elif args.requesters:
  ### PRINT REQUESTERS ##
  sortedReq = dict(sorted(rqstrs.items(), key=lambda x: x[1], reverse=True))
  # print(sortedReq)
  for value in sortedReq:
    print(value, "\t", sortedReq.get(value))

## PRINT RESOURCES w/ TOP NUM ##
if args.resources and args.number or args.errors and args.number:
  topNum = args.number[0]
  top = int(topNum)
  sortedReso = dict(sorted(resours.items(), key=lambda x: x[1], reverse=True))
  if len(sortedReso) > topNum:
    for i in range(top):
      print(list(sortedReso.keys())[i], "\t", list(sortedReso.values())[i])
  else:
    print("\nError: Number needs to be smaller.\n")
elif args.resources or args.errors:
  ### PRINT RESOURCES ##
    sortedReso = dict(sorted(resours.items(), key=lambda x: x[1], reverse=True))
    for value in sortedReso:
      print(value, "\t", sortedReso.get(value))

## PRINT HOURLY w/ TOP NUM ##
if args.hourly and args.number:
  topNum = args.number[0]
  top = int(topNum)
  sortedHr = dict(sorted(dateDict.items(), key=lambda x: x[1], reverse=True))
  if len(dateDict) > topNum:
    for i in range(top):
      print(list(sortedHr.keys())[i], "\t", list(sortedHr.values())[i])
  else:
    print("\nError: Number needs to be smaller.\n")
elif args.hourly: ## PRINT HOURLY ##
  sortedHr = dict(sorted(dateDict.items(), key=lambda x: x[1], reverse=True))
  for value in sortedHr:
    print(value, "\t", sortedHr.get(value))

print("\n")
