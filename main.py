import re
import os
import shutil


def copy(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    shutil.copyfile(src, dst)


def replacer(file_name, source, destenition):
    with open(file_name, 'r+',  encoding="utf8") as file:
        filedata = file.read()

        # Replace the target string
    filedata = filedata.replace(source, destenition)

    # Write the file out again
    with open(file_name, 'w',  encoding="utf8") as file:
        file.write(filedata)


STATIC_PRE = ('assets',)
STATICLY_TAGS = ('src', 'href',)
WORKING_DIRECTORY = './'
BACKUP_DIRECTORY = './test'
staticly_pattern_template = '('
if len(STATICLY_TAGS) > 1:
    for index, element in enumerate((STATICLY_TAGS)):
        if index != (len(STATICLY_TAGS) - 1):
            staticly_pattern_template += element+"|"
        else:
            staticly_pattern_template += element+')'
    STATICLY_TAGS = staticly_pattern_template
else:
    STATICLY_TAGS = STATICLY_TAGS[0]
if len(STATIC_PRE) > 1:
    static_pre_template = '('
    for index, element in enumerate((STATIC_PRE)):
        if index != (len(STATIC_PRE) - 1):
            static_pre_template += element+"|"
        else:
            static_pre_template += element+')'
    STATIC_PRE = static_pre_template
else:
    STATIC_PRE = STATIC_PRE[0]
regex_pattern = rf'''(src|href)=('|"{STATIC_PRE}.*?('|"))'''


static_pattern = re.compile(regex_pattern)
# all html files in directorys
all_html_files_in_directory = [x for x in os.listdir(WORKING_DIRECTORY) if
                               x.split('.')[-1] in ['html', 'htm']]
# get backup
for template in all_html_files_in_directory:
    copy(os.path.join(WORKING_DIRECTORY, template), BACKUP_DIRECTORY)
temp_file = ""
# edit all files static files
for template in all_html_files_in_directory:
    temp_file = "{% load static %}"
    with open(os.path.join(WORKING_DIRECTORY, template), 'r+', encoding="utf8") as file:
        lines = file.readlines()
        matches = []
        for line in lines:
            matches.append(re.findall(regex_pattern, line))
        matches = [x[0][1].replace('"', '') for x in matches if len(x) == 1]
        matches = set(matches)
        print(matches)
        for i in matches:
            replacer(os.path.join(WORKING_DIRECTORY, template), i, "{% static '" + i + "'  %}")
