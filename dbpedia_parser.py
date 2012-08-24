"""have to install the dbpediakit from https://github.com/ogrisel/dbpediakit"""
import dbpediakit as dbk
import dbpediakit.archive

def search(keyword1 = "test1", keyword2 = "test2"):
    archive_file = dbk.archive.fetch("persondata")
    #archive_file

    tuples = dbk.archive.extract_text(archive_file)
    #tuples

    for record in tuples:
        if record.title == keyword1 or record.title == keyword2:
            if record.text.find(keyword1) == -1 or record.text.find(keyword2) == -1:
                print record   
