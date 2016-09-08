from analysis import *
# for t in tblnames:
#     splittable(usrs, t, conn, splitdict, filepaths)

##load sample data to desk session labeling for an auth session

#def labelauthsessions(header, filepaths, sample)
#def labelsessions(df,tstamplist)
filelist = ["U8946"]
sampleusr = unpkl(os.path.join(filepaths['auth'], filelist[0]))
sampledf = pd.DataFrame(sampleusr, columns = headers['auth'])
samplecomp = unpkl(os.path.join(filepaths['auth'], "U2109"))
samplecompdf = pd.DataFrame(samplecomp, columns = headers['auth'])

#labelauthsessions(headers['auth'], filepaths, filelist)
def labelsessions(df,tstamplist):
    """Label the sessions for a unique user or computer."""
    i = 0
    for s in tstamplist:
        #print(s)
        # if tstamplist[i] == tstamplist[i + 1]:
        #     print("Tstamps equal. Next.")
        #     i += 1
        #     next
        if i == 0:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("First item")
            # print(i)
            sub = df[(df.tstamp < tstamplist[i])]
            df.loc[sub.index,'session'] = i
            i += 1
        elif i >= 1 and i < len(tstamplist) - 1:
#            print(i)
#            print("Stuck in the middle with you." + str(i >= 1 and i < len(tstamplist) - 1))
            sub = df[(df.tstamp >= tstamplist[i -1]) & (df.tstamp < tstamplist[i])]
            if len(sub) == 0:
                # print("///////")
                # print("Nothing in tstamp window")
                #df.loc[sub.index,'session'] = 0
                next
            #if len(sub) == 0:
            df.loc[sub.index,'session'] = i
            i += 1
        elif i == len(tstamplist) - 1:
            print("on last item")
            print(i)
            sub = df[(df.tstamp >= tstamplist[i])]
            df.loc[sub.index,'session'] = i
            #print(tstamplist[i])
            print("Filelist looped")

def labelNONAUTHsessions(headers ,filepaths, tstamps, sample = usrs, tblnames = tblnames):
    for t in tblnames:
        filelist = listdir(filepaths[t])
        for f in filelist:
            if f.rstrip('.pkl') in sample:
                try:
                    data = sorted(unpkl(os.path.join(filepaths[t],f)), key=itemgetter(1))
                except EOFError:
                    print("File " + f + " is empty!")
                    emptyfiles.append(f)
                    pkl(emptyfiles, '/media/pcgeller/SharedDrive/weirdo/workspace/emptyfiles.pkl')
                    next
                df = pd.DataFrame(data, columns = headers[t])
                df.sort(columns = 'tstamp')
                labelsessions(df,tstamps[f.rstrip('.pkl')])
                pkl(df, os.path.join(filepaths['dataframes'],t,(f + '.pkl')))
            else:
                print("not in sample")
                next

def labelauthsessions(header, filepaths, sample):
    """Open unique user and computer pickle from auth table.
    Read file as dataframe.  Loop through and extract AuthMap events and
    the timestamp they occured. Store tstamps in dictionary keyed on unique usr/comp
    Pickle dataframe. <- worth it?"""
    filelist = listdir(filepaths['auth'])
    # filelist.remove('$RECYCLE.BIN')
    filelist = [x for x in filelist if x in sample]
    #filelist = sample
    tstampdict = {}
    emptyfiles = []
    notfound = []
    memerror = []
    t = 'auth'
    for f in filelist:
        #if os.path.isfile(os.path.join(filepaths['auth'],f)) == False:
        #    print('file doesnt exist')
            try:
                data = sorted(unpkl(os.path.join(filepaths['auth'],f)), key=itemgetter(1))
            except EOFError:
                print("File " + f + " is empty!")
                emptyfiles.append(f)
                next
            except IOError:
                print("File " + f + " not found.")
                notfound.append(f)
                next
            except MemoryError:
                print("MEMORY ERROR with file: " + f)
                memerror.append(f)
                next
            df = pd.DataFrame(data, columns = header)
            df.sort(columns = 'tstamp')
            authdata = df.loc[df['authorient'] == "AuthMap"]
            tstamplist = authdata['tstamp']
            tstamplist = sorted(tstamplist)
            tstampdict[f] = tstamplist
            labelsessions(df, tstamplist)
            pkl(df, os.path.join(filepaths['dataframes'],t,(f + 'df.pkl')))
        #else:
            #print("File " + f + " already exists.")
            next
    pkl(emptyfiles, '/media/pcgeller/SharedDrive/weirdo/workspace/emptyfiles.pkl')
    pkl(notfound, os.path.join(filepaths['workspace'],f))
    pkl(memerror, os.path.join(filepaths['workspace'],f))
    pkl(tstampdict, os.path.join(filepaths['workspace'],'tstampdict2.pkl'))
    return(tstampdict)

#tstampsusrs = unpkl(os.path.join(filepaths['workspace'],'usrtstampdict.pkl'))

#tstamps = unpkl('/home/pcgeller/workspace/weirdo/tstampdict2.pkl')

tstamps = labelauthsessions(headers['auth'],filepaths,usrs)
labelNONAUTHsessions(headers,filepaths,tstamps,usrs,tblnames)
