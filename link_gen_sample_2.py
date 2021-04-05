from link_combine import combine
from link_test import readFileByLineNums
import shutil, os
files_donor = ['R$anim.smali',
    'R$attr.smali',
    'R$bool.smali',
    'R$color.smali',
    'R$dimen.smali',
    'R$drawable.smali',
    'R$id.smali',
    'R$integer.smali',
    'R$layout.smali',
    'R$menu.smali',
    'R$string.smali',
    'R$style.smali',
    'R$styleable.smali',
    'R$xml.smali']

files_host = ['R$anim.smali',
    'R$attr.smali',
    'R$bool.smali',
    'R$color.smali',
    'R$dimen.smali',
    'R$drawable.smali',
    'R$id.smali',
    'R$integer.smali',
    'R$interpolator.smali',
    'R$layout.smali',
    'R$mipmap.smali',
    'R$string.smali',
    'R$style.smali',
    'R$styleable.smali']

path_donor = '/Users/sakshamarora/Desktop/grafting/generated_sample_2/leak/smali/com/robocleansoft/boostvscleanapp/'
path_host = '/Users/sakshamarora/Desktop/grafting/generated_sample_2/host_mare/smali_classes2/com/example/host_mare/'

# .annotation system Ldalvik/annotation/MemberClasses;

try:
    donor_resource_master = open(path_donor + 'R.smali', 'r')
    host_resource_master = open(path_host + 'R.smali', 'r')
    donor_resource_master_lines = donor_resource_master.readlines()
    host_resource_master_lines = host_resource_master.readlines()
except:
    print("Could not open master resource files")

donorNum = 0
hostNum = 0
donorStart = 0
donorEnd = 0
hostStart = 0
hostEnd = 0
donorClassName = ''
for line in donor_resource_master_lines:
    if line[0:52] == '.annotation system Ldalvik/annotation/MemberClasses;':
        donorStart = donorNum + 2

    if line[0:15] == '.end annotation':
        donorEnd = donorNum - 2

    if line[0:6] == '.class':
        donorClassName = line

    donorNum += 1

donor_package_name = ''
for word in donorClassName.strip().split(" ")[-1].strip().split("/")[:-2]:
    donor_package_name += word + "/"
donor_package_name += donorClassName.strip().split(" ")[-1].strip().split("/")[-2]
donor_package_name = donor_package_name.strip().split(";")[0]

donorResources = readFileByLineNums(path_donor + 'R.smali', donorStart, donorEnd)
donorResourcesCleaned = []

for i in range(1, len(donorResources)):
    donorResourcesCleaned.append(donorResources[i].split(",")[0].split("/")[-1])

hostClassName = ''
for line in host_resource_master_lines:
    if line[0:52] == '.annotation system Ldalvik/annotation/MemberClasses;':
        hostStart = hostNum + 2

    if line[0:15] == '.end annotation':
        hostEnd = hostNum - 2

    if line[0:6] == '.class':
        hostClassName = line

    hostNum += 1

host_package_name = ''
for word in hostClassName.strip().split(" ")[-1].strip().split("/")[:-2]:
    host_package_name += word + "/"
host_package_name += hostClassName.strip().split(" ")[-1].strip().split("/")[-2]
host_package_name = host_package_name.strip().split(";")[0]

hostResources = readFileByLineNums(path_host + 'R.smali', hostStart, hostEnd)
hostResourcesCleaned = []

for i in range(1, len(hostResources)):
    hostResourcesCleaned.append(hostResources[i].split(",")[0].split("/")[-1])

try:
    combine_file = open('R_combine.smali', 'w')
except FileNotFoundError:
    print("Error opening file")

beforeHost = readFileByLineNums(path_host + 'R.smali', 0, hostEnd)
afterHost = readFileByLineNums(path_host + 'R.smali', hostEnd + 1, hostNum)

for line in beforeHost:
    combine_file.write(line)

for i in range(1, len(donorResources) - 1):
    if donorResourcesCleaned[i] not in hostResourcesCleaned:
        combine_file.write(hostResources[1][0:30] + '/' + donorResourcesCleaned[i] + '\n')

for i in range(1, len(donorResources) - 1):
    if donorResourcesCleaned[i] not in hostResourcesCleaned:
        shutil.move(path_donor + donorResourcesCleaned[i][0:-1] + '.smali', path_host)

for line in afterHost:
    combine_file.write(line)

directory = '/Users/sakshamarora/Desktop/grafting/generated_sample_2/leak/smali/com/robocleansoft/boostvscleanapp'
files_host = []
for filename2 in os.listdir('/Users/sakshamarora/Desktop/grafting/generated_sample_2/host_mare/smali_classes2/com/example/host_mare/'):
    files_host.append(filename2)
for filename in os.listdir(directory):
    if filename.endswith(".smali"):
        read_file = open(directory + '/' + filename, 'r')
        lines = read_file.readlines()
        write_file = open(directory + '/' + filename, 'w')
        for line in lines:
            write_file.write(line.replace(donor_package_name, host_package_name))
        if filename not in files_host and filename[0:-7] not in donorResourcesCleaned:
            shutil.move(os.path.join(directory, filename), os.path.join('/Users/sakshamarora/Desktop/grafting/generated_sample_2/host_mare/smali_classes2/com/example/host_mare/', filename))
