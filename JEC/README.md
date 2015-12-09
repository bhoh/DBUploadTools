# DBUploadTools
This repository contains additional files and tools which are helpful/necessary for uploading JEC to the CMS conditions database(s). These tools are meant to augment those already contained within the JetMETCorrections/Modules sub-package. In some cases these are new tools not included in JetMETCorrections/Modules and in some cases these are modified tools that already exist in that sub-package.

## Create a database from text files

You need a bunch a text files to create a database. This guide assumes you already have all the corrections. The CMSSW configuration you need to run is ``createDBFromTxtFiles.py``. You can (and probably need) to edit this file to customize the jet algorithms put in the database. By default it's AK4 and AK8, for non-CHS, CHS and PUPPI. Follow these steps to create a new database:

 - Setup a CMSSW release :

```bash
export SCRAM_ARCH slc6_amd62_gcc791
cmsrel CMSSW_7_5_2
cd CMSSW_7_5_2/src
cmsenv

git cms-addpkg JetMETCorrections/Modules
git clone https://github.com/cms-jet/DBUploadTools.git JetMETCorrections/DBUploadTools
git clone https://github.com/cms-jet/JECDatabase.git JetMETCorrections/JECDatabase

scram b -j 4

cd JetMETCorrections/DBUploadTools
```

 - Update the ``JECDatabase`` repository with the new set of text files. Go to ``JetMETCorrections/JECDatabase/textFiles/`` and create a new folder corresponding to the new era. Usually, you'll want to copy the folders from the previous era into a new folder, and just update the files that have changed. Don't forget to commit your changes! Ideally, you'll have two commits
   
    - The first one creating the new era for data and MC, which is just a copy of the previous era. Do not forget to rename all the text files to change the era name. You can use the ``rename`` command for that: ``rename <old era> <new era> *.txt``
    - The second updating the files. Please indicate in your commit message a reference to the mail / hypernews message. If you need to duplicate some files, please use symbolic links instead of hard copies. It's easier to track which files is a copy of which one. See the ``Summer15_25nsV3_DATA`` era for an example.

 - Go back to the ``DBUploadTools`` folder. We'll start by creating the MC database. Copy the era folder you need from the ``JECDatabase`` to your current directory:

```bash
cp -r ../JECDatabase/textFiles/Summer15_25nsV3_DATA data
```

Change the folder name to yours. The destination **must** be ``data`` for the script to work. Unfortunately, CMSSW does not handle very well symbolic links. Before running the command, you'll need to convert symbolic links to hard links. Just run the following command:

```bash
./removeSymlinks.sh data
```

 - To ensure everything works, redo a scram build, ``scram b -j4``

 - Now, just execute the CMSSW command to create the database:

```bash
cmsRun createDBFromTxtFiles.py era=Summer15_25nsV3_DATA path=JetMETCorrections/DBUploadTools/data/
```

Change the era to yours. You should now have a database in your current directory.

 - For MC, just restart this guide, changing DATA to MC.

## Inspect the database

You can use the following command to inspect the content of the database:

```bash
conddb --db Summer15_25nsV3_DATA.db search Jet
```
