#input is two lists - first with a set of questions; second with a set of corresponding answers

def test_set(test_questions = [], test_answers = []):
    questions = []
    answers = []
    
    questions.append("Was Warhol a filmmaker?")
    answers.append("Yes")#Andy Warhol was an American artist, avant-garde filmmaker, writer and social figure
    
    questions.append("Who was the second president of St. Ambrose University?")
    answers.append("John Flannagan")

    questions.append("When was Albert Einstein born?")
    answers.append("1879")#14 March 1879

    questions.append("Was Bouchard a Australian ecologist?")
    answers.append("No");#Canadian/Quebec ecologist

    questions.append("Which state did Boo Ellis used to play for?")
    answers.append("Minneapolis")

    questions.append("Who was Edward Wasilewski?")
    answers.append("Member of Anti-communist resistance in Poland")

    questions.append("Was Hamad Al Tayyar a football player?")
    answers.append("Yes")

    questions.append("Who was John Albert Gardner?")
    answers.append("American double murderer")

    #print str(questions)
    #print str(answers)

    #answer to be returned
    ans = []
    #loop through the test questions and match with the questions in the test set
    #compare with the relavant test answer
    #return two arrays: questions array, right answers array: true if test answer is correct; correct answer otherwise
    for tq in test_questions:
        if tq in questions:
            q_index = questions.index(tq)
            tq_index = test_questions.index(tq)
            if answers[q_index] == test_answers[tq_index]:
                ans.append(True)
            else:
                ans.append(answers[q_index])
    return test_questions, ans

#let's try it out. q = sample set ot test questions; a = sample set of corresponding answers
q = ["Was Warhol a filmmaker?", "When was Albert Einstein born?"]
a = ["No", "1879"]
b, c = test_set(q, a)
print "Questions: " + str(b)
print "Answers: " + str(c)