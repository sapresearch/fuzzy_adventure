"""have to install the dbpediakit from https://github.com/ogrisel/dbpediakit"""
import sys
sys.path.append('./external/dbpediakit')
import dbpediakit as dbk
import dbpediakit.archive

#search method with 3 arguments
def search(keyword1, keyword2):
    archive_file = dbk.archive.fetch("persondata")
    tuples = dbk.archive.extract_triple(archive_file)
    for record in tuples:
        #print record.id + " " + record.title + " " + record.text
        arr = [keyword1, keyword2]
        for keyword in arr:
            if record.title.find(keyword) != -1:
                arr.remove(keyword);
                if record.text.find(arr[0]) != -1:
                    print record

#method overloading: with 3 arguments
def search(keyword1, keyword2, keyword3):
    archive_file = dbk.archive.fetch("persondata")
    tuples = dbk.archive.extract_triple(archive_file)
    
    #found = false
    for record in tuples:
        #print record.id + " 2. " + record.title + " 3. " + record.text
        arr = [keyword1, keyword2, keyword3]
        for keyword in arr:
            if record.id.find(keyword) != -1:
                arr.remove(keyword);
                if record.title.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.text.find(arr[0]) != -1:
                        print record
                elif record.text.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.title.find(arr[0]) != -1:
                        print record
                elif record.title.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.text.find(arr[0]) != -1:
                        print record
                elif record.text.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.title.find(arr[0]) != -1:
                        print record
            elif record.title.find(keyword) != -1:
                arr.remove(keyword);
                if record.id.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.text.find(arr[0]) != -1:
                        print record
                elif record.text.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.id.find(arr[0]) != -1:
                        print record
                elif record.id.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.text.find(arr[0]) != -1:
                        print record
                elif record.text.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.id.find(arr[0]) != -1:
                        print record
            elif record.text.find(keyword) != -1:
                arr.remove(keyword);
                if record.id.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.title.find(arr[0]) != -1:
                        print record
                elif record.title.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.id.find(arr[0]) != -1:
                        print record
                elif record.id.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.title.find(arr[0]) != -1:
                        print record
                elif record.title.find(arr[0]) != -1:
                    arr.remove(arr[0])
                    if record.id.find(arr[0]) != -1:
                        print record

        #arr1 = [keyword1, keyword2, keyword3]
        #arr2 = [record.id, record.title, record.text]
        #print arr1
        #print arr2
        #diff = set(arr1) - set(arr2)
        #if not diff:
        #    print record