import dbpediakit as dbk
import dbk.archive

archive_file = dbk.archive.fetch("long_abstracts")
archive_file

tuples = dbk.archive.extract_text(archive_file)

first = tuples.next()
first.id

first.text[:60] + u"..."
u'Autism is a disorder of neural development characterized by ...'
