"""have to install the dbpediakit from https://github.com/ogrisel/dbpediakit"""
import dbpediakit as dbk
import dbpediakit.archive

def search(keyword1 = "test1", keyword2 = "test2"):
    archive_file = dbk.archive.fetch("persondata")
    #archive_file

    tuples = dbk.archive.extract_text(archive_file)
    #tuples

    for record in tuples:
        arr = [keyword1, keyword2]
        for keyword in arr:
            if record.title.find(keyword) != -1:
                arr.remove(keyword);
                if record.text.find(arr[0]) != -1:
                    print record
