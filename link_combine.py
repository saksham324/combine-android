from link_test import readFileByLineNums

def combine(hostFile, donorFile):
    try:
        file = open(hostFile, 'r')
        lines = file.readlines()
    except FileNotFoundError:
        print("File not found")
    start = 0
    end = 0
    lineNum = 1
    for line in lines:
        if line[0:15] == "# static fields":
            start = lineNum
        if line[0:16] == "# direct methods":
            end = lineNum - 1
        lineNum += 1


    beforeFields = readFileByLineNums(hostFile, 1, start - 1)
    afterFields = readFileByLineNums(hostFile, end + 1, lineNum)

    fields = readFileByLineNums(hostFile, start, end)
    variables_host = {}
    for line in fields:
        list = line.split(" ")
        if len(list) > 2:
            variables_host[line] = list[-3]
    #
    # try:
    #     write_file = open("combined.smali", 'w')
    try:
        host = open(donorFile, 'r')
        lines_host = host.readlines()
    except FileNotFoundError:
        print("File not found")

    start_host = 0
    end_host = 0
    lineNum_host = 1
    for line in lines_host:
        if line[0:15] == "# static fields":
            start_host = lineNum_host
        if line[0:16] == "# direct methods":
            end_host = lineNum_host - 1
        lineNum_host += 1

    beforeFieldsHost= readFileByLineNums(donorFile, 1, start_host - 1)
    afterFieldsHost = readFileByLineNums(donorFile, end_host + 1, lineNum_host)

    fieldsHost = readFileByLineNums(donorFile, start_host, end_host)
    variables_donor = {}
    for line in fieldsHost:
        list = line.split(" ")
        if len(list) > 2:
            variables_donor[line] = list[-3]

    try:
        combine = open(hostFile, 'w')
    except FileNotFoundError:
        print("Error opening file")

    for line in beforeFields:
        combine.write(line)

    for line in fields:
        if line in variables_host.keys() and variables_host[line] not in variables_donor.values():
            combine.write(line)

    for line in fieldsHost:
        combine.write(line)

    for line in afterFields:
        combine.write(line)

combine("R$anim.smali", "R$anim_donor.smali")