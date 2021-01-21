import compileall
import sys,time,os,shutil,re


SourceFileList=['src\\choice_7.py', \
                'src\\netbug.py' \
                ]

OtherFileList=['src\\choice_main.bat']

SourceParentDir='..'
SourceChildDirList=['src']

DestDir='..\\Dest'
DestSourceDir='..\\SourceExe'


# 删除目标目录如果存在

if os.path.exists(DestDir):
    shutil.rmtree(DestDir, True)
    
if os.path.exists(DestSourceDir):
    shutil.rmtree(DestSourceDir, True)

os.mkdir(DestDir)
os.mkdir(DestSourceDir)

for i in SourceFileList:
    FileFullName = SourceParentDir + '\\' + i
    FromPycFileName = SourceParentDir + '\\' + i.replace('.py','.pyc')
    TempName = re.findall('[^<>/\\\|:""\*\?]+\.\w+$',i)
    ToDestName = DestDir + '\\' + TempName[0].replace('.py','.pyc')
    ToSourceName = DestSourceDir + '\\' + TempName[0]
    print(FileFullName)
    print(FromPycFileName)
    print(ToDestName)
    print(ToSourceName)
    compileall.compile_file(FileFullName, force=True, legacy = True)
    shutil.copy(FileFullName,ToSourceName)
    shutil.copy(FromPycFileName,ToDestName)
    os.remove(FromPycFileName)

for i in OtherFileList:
    FileFullName = SourceParentDir + '\\' + i
    TempName = re.findall('[^<>/\\\|:""\*\?]+\.\w+$',i)
    ToSourceName = DestSourceDir + '\\' + TempName[0]
    ToDestName = DestDir + '\\' + TempName[0]
    shutil.copy(FileFullName,ToSourceName)
    shutil.copy(FileFullName,ToDestName)
