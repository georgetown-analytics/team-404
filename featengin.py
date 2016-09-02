from analysis import *

def buildfeatflows(dfFilepaths, table = 'flows'):
    files = listdir(dfFilepaths[table])
    for f in files:
        data = unpkl(os.path.join('dfFilepaths',f))
        print(type(data))
        numsessions = data.sessions.unique()

        
