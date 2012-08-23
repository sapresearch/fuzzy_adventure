"""have to install the dbpediakit from https://github.com/ogrisel/dbpediakit"""
import dbpediakit as dbk
import dbk.archive

archive_file = dbk.archive.fetch("peopledata")
archive_file

tuples = dbk.archive.extract_text(archive_file)

first = tuples.next()
first.id
first.text[:60] + u"..."
