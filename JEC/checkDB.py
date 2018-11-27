import os

Era= "Fall17_17Nov2017"
for x in ["B", "C", "DE", "F"]:
  cmd = "conddb --db "+Era+x+"_V32_DATA.db listTags"
  print cmd
  os.system(cmd)



# For MC
cmd = "conddb --db "+Era+"_V32_MC.db listTags"
print cmd
os.system(cmd)
