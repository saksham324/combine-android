import os
def readFileByLineNums(filename, start, end):
    output = []
    try:
        file = open(filename, 'r')
        file_lines = file.readlines()
    except FileNotFoundError:
        print("File "+filename+" not found")
    lineNum = 1
    for line in file_lines:
        if lineNum >= start and lineNum <= end:
            output.append(line)
        lineNum += 1
    return output

try:
    donor = open('R_donor.smali', 'r')
    host = open('R_host.smali', 'r')
    host_lines = host.readlines()
    donor_lines = donor.readlines()
except FileNotFoundError:
    print("File not found")

def computeCredentials(lines):
	class_name = ""
	lineNum = 1
	membersStart= None
	membersEnd = None
	membersFlag = False
	member_classes = []
	for line in lines:
		# print(line[0:6])
		if line[0:6] == '.class':
			class_name = line
			# print(class_name.strip().split(" ")[-1].strip())
		# print(line[0:11])
		if line[0:11] == ".annotation":
			temp = line.strip().split("/")
			# print(temp)
			if temp[-1] == 'MemberClasses;':
				membersStart = lineNum + 1
				membersFlag = True
		# print(line[0:15])
		if line[0:15] == ".end annotation" and membersFlag:
			membersEnd = lineNum - 1
		lineNum += 1
	member_classes = readFileByLineNums('R_donor.smali', membersStart, membersEnd)

	member_classes = member_classes[1:len(member_classes) - 1]
	member_classes = [x.strip().split(" ")[0].strip().split("/")[-1].strip().split(";")[0] for x in member_classes]
	member_classes_set = set(member_classes)
	package_name = ""
	for word in class_name.strip().split(" ")[-1].strip().split("/")[:-2]:
		package_name += word + "/"
	package_name += class_name.strip().split(" ")[-1].strip().split("/")[-2]
	package_name = package_name.strip().split(";")[0]
	return package_name, member_classes_set, class_name

host_package, host_members, host_class = computeCredentials(host_lines)
donor_package, donor_members, donor_class = computeCredentials(donor_lines)
