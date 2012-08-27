"""have to install the dbpediakit from https://github.com/ogrisel/dbpediakit"""
import sys
sys.path.append('./external/dbpediakit')
import dbpediakit as dbk
import dbpediakit.archive

def search(keyword1 = "test1", keyword2 = "test2"):
    archive_file = dbk.archive.fetch("persondata")
    tuples = dbk.archive.extract_triple(archive_file)
    for record in tuples:
        arr = [keyword1, keyword2]
        for keyword in arr:
            if record.id.find(keyword) != -1:
                arr.remove(keyword);
                if record.title.find(arr[0]) != -1:
                    print record
