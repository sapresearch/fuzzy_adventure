import string 

# import fuzzy_adventure.query_decomposition 
# import triplet_extraction
import keyWordsExtraction
from stanford_client import to_tree
import penn_treebank_node

log_Q1 = open('/home/I837185/Puntis_Practices/logFile1.txt', 'w')
log_Q2 = open('/home/I837185/Puntis_Practices/logFile2.txt', 'w')

Questions_List_Type1 = [
"Who is the most productive employee on my team?","Who is the most efficient employee on my team?","Which employee on my team has the highest productivity?","Who is the best?",
"Who's the best employee?","Who can close the most tickets the fastest?","Who is the person that contribute the most to the success of my team?","Tell me the name of the most productive person on my team.",
"Who is the most efficient and effective at their job? ","Who consistently proves they can provide quality work/support on a regular basis? ","Who is always there to solve complex issues? ",
"Which member on my team is closing the most number of open ticket? ","Who is the most open tickets closer member on the team? ","Considering the most number of open tickets closed, who is the most productive member of the team? ",
"Who on the team, is the person that close the biggest amount of open tickets? ","Who deliver most in my team?","Who is the most efficient people in my team ","Who always close most number of open tickets in a sprint ?",
"Who is the person you will assign most important task to?","Which person on my team closes the most tickets? ","Which one of my team members is most productive? ",
"Who, in my team, works fastest? ","Which person on my team closes the most tickets? ","What person closes the most tickets? ","What programmer is the fastest at closing tickets? ",
"Which team member closes the most tickets? ","Who is the most productive on my team?","What is the name of the top contributor in the group? ","What is the first in a list of team members ordered by effectiveness? ",
"Whose tickets are dealt with most swiftly? ","Who is number 1 in the item management system? ","Who clears problems the quickest? ","Rank my team on problem resolution time? ","Show me the productivity information about my team",
"Who is the number 1 contributor on the team? ","Who on the team solves the most issues? ","Who is the top closer on the team? ","Name the most productive person on the team ","Name the most productive person on your team. ",
"Who is the most productive on your team? ","In your team, who would you say is the most productive person. ","Who in your team closes the most open tickets on average? ","who is the best developer in my team ",
"who closes more tickets in Jira ","who is the most productive developer ","who is the fastest developer ","Who is the most productive team member? ","Who is the most efficient person in my team? ",
"Who has the best productivity in my team? ","Who knows Jira best in my team? "," Who solve the most number of open tickets? "," Who has the deepest knowledge of the project? "," Who answer the most questions for the project? ","Who is assigned to the most number of open tickets?"," Who is the best developer ",
"Who is the fastest developer ","Which developer is the most productive "," Which developer is the fastest "]

Questions_List_Type2 = ["What components are contributing the most to my backlog?","What component are taking part the most to my backlog? ","What component has the maximum contribution to my backlog? ",
"What components delay my team's work the most? ","What components take most time to get resolved?","From all the opened tickets, what software causes the most delay? ","What components use most of my ressources? ",
"What component makes up the largest part of my backlog? ","What software is slowing us down? ","What manual processes are slowing me down the most? ","What system(s) are not working properly today? ","How many times did excel crash today? ",
"Did I have any support from my supervisor today? ","What software components contribute the most to slowing down the team?","By which components the team is the most slow down? ","Which software elements contribute the most in your team backlog? "
"Did I have any support from my supervisor today? ","Which component has most problem ","Which component I need to assign more people to ?","Which ticket component are most time consuming ","Which component i need to monitor most to see how to improve it ",
"What software components hinder my team most? ","What components are the biggest obstacles to my team's productivity? ","What software components hinder my team's productivity the most? ","What are the main software components that slow my team down? ",
"What software creates the tickets that slow us down the most? ","Which components are slowing down my team? ","What component is my team struggling with? ","What software components are slowing down my backlog? ",
"Which areas of code are generating the most problems? ","Which features are causing the most work? ","Which domain is most trouble? ",
"Which modules are the most difficult to maintain? ","Which modules give us the most trouble? ","What modules do we spend a lot of time on?","What are the significant items that are slowing the team down? ",
"What are the key factors to my backlog? ","What is slowing down my team? ","List the components that slow my system the most ","What software components are slowing down the team the most? ",
"Name a few components that are contributing to slowing down the team? ","What software components are contributing the most to the backlog of the team? ","To what components is your backlog attributable (in general)? ",
"which components contribute most to my backlog ","which components are adding to my work load ","what are the modules that contribute usually to my backlog ?","what modules make me work more?",
"What components have the greatest impact on my backlog? ","What components are weighting the most in my backlog? ","what items are the most significant in my backlog?",
"What items are the most demanding in my backlog?","what components have the highest priority?","what components are used most frequently? ","what components have the highest complexity? ",
"what components take the longest time to implement?","On which component do I work the most?","Which component takes the most time?","Which component requires the most work?",
"On which component do I spend the most time?"]

for question in Questions_List_Type1:
        log_Q1.write("\r\n=========================================================================================================\r\n")
        log_Q1.write(question+'\r\n')
        tree = to_tree(question+'\r\n')
        log_Q1.write(tree+'\r\n')
        # log_Q1.write(tree+'\r\n')
        # log_Q1.write(tree+'\r\n')
        root = penn_treebank_node.parse(tree)
        keyWords, question_type = keyWordsExtraction.keyWordsExtraction(root)
        if not keyWords:
                log_Q1.write("No triplet found! \r\n")
        else:
            temp = []
            for w in keyWords:
                if w != None:
                    temp.append(str(w.word))
            q_noPunc = question.translate(string.maketrans("",""), string.punctuation)
            words = q_noPunc.split(" ")
            for w in words:
                if w in temp:
                    log_Q1.write (w+ ',')
        log_Q1.write ('\r\nLooking for = ')
        log_Q1.write (str(question_type))


for question in Questions_List_Type2:
        log_Q2.write("\r\n=========================================================================================================\r\n")
        log_Q2.write(question+'\r\n')
        tree = to_tree(question+'\r\n')
        log_Q2.write(tree+'\r\n')
        # log_Q2.write(tree+'\r\n')
        root = penn_treebank_node.parse(tree)
        keyWords, question_type = keyWordsExtraction.keyWordsExtraction(root)
        if not keyWords:
                log_Q2.write("No triplet found! \r\n")
        else:
            temp = []
            for w in keyWords:
            	if w != None:
                	temp.append(str(w.word))
            q_noPunc = question.translate(string.maketrans("",""), string.punctuation)
            words = q_noPunc.split(" ")
            for w in words:
                if w in temp:
                    log_Q2.write (w+ ',')
                        # w.word
        log_Q2.write ('\r\nlooking for = ')
        log_Q2.write (str(question_type))
