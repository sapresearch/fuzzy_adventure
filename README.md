fuzzy_adventure
===============

A question-answering system.

Setup and Installation
======================

** On Ubuntu:

  To get it running, you'll need jython to run the Stanford Parser:

		sudo apt-get install jython

	Then untar the Stanford Parser:

		tar -zxvf stanford-parser-2008-10-26.tgz

	Install the dbpediakit from https://github.com/ogrisel/dbpediakit.

		git clone https://github.com/ogrisel/dbpediakit


To get started, type 'jython question_parser.py' and then follow the prompt.

** Make sure that you have unzipped the EN folder in “\git\fuzzy_adventure\fuzzy_adventure\external”. (EN is an open source library that our system uses to complete some Natural Language Processing task.)


Running the System
======================


The system has two different Modules which could be evaluated separately; NLIDB module and NLIDB+SQL(whole system) module

** To Run the Whole system using the shell:

-Change the directory to: ‘~/git/fuzzy_adventure/fuzzy_adventure’
-Run  executable.py
-write a question from the list of the questions we have. 
Such as ‘who is the most effective employee? ‘ . List of the questions could be found in “Z:\git\fuzzy_adventure\fuzzy_adventure\context_based_data\ questionsByManagers” and ““Z:\git\fuzzy_adventure\fuzzy_adventure\context_based_data\Survey_Result”.
-enter your user/pass to connect to Hana

If you run the system as  ‘python executable.py --help’ you get all the options you have. For instance, running the system with --test  parameter will let you to run the Naïve Baye’s Experiment to see the accuracy of the system on the current dataset of questions:
-python executable.py --test


** To Run the Whole System Using the Gui:
Needs more work!


** To Run the NLIDB module:
Running this module will help you to figure out about the keywords that our system feeds into the SQL module for debugging.
-Change your directory to “~/git/fuzzy_adventure/fuzzy_adventure/query_decomposition/nlp_system”
-Run runner.py



