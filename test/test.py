import sys
sys.path.append("../")
import fuzzy_adventure
#test method
def test():
    questions, answers = test_data()
    correct = 0.0
    for q in questions:
        print q
        real_answer = questions.index(q)
        predicted_answer, _, _, _, _, _, _ = fuzzy_adventure.ask_question(q)
        print predicted_answer
        if real_answer == predicted_answer:
            correct += 1

    accuracy = correct / float(len(questions)) *100.0
    return accuracy

#standard set of questions and answers (real)
def test_data():
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

    questions.append("Who was James A. Walker?")
    answers.append("Confederate Army general")
    
    return questions, answers

print test()
