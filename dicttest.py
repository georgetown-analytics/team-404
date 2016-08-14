from os import listdir
from os.path import isfile, join

path = '/home/pcgeller/weirdo'
filelist = [f for f in listdir(path) if isfile(join(path,f))]

def mkfiledictionary(path):
        """Make dictionary of files and their byte size and readable size\
        Sorted by their filesize in bytes."""
        dictionary = {}
        for f in listdir(path):
                bytesize = os.path.getsize(join(path,f))
                rablesize = size(bytesize)
                #dictionary.update = ({bytesize: rablesize})
                dictionary[f] = [bytesize, rablesize]
                dictionary = sorted(dictionary, key=itemgetter(0))
