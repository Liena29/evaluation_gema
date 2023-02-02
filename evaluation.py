import streamlit as st
import random
import json
import uuid

class Appraisal:
    def __init__(self):
        if 'step' not in st.session_state:
            st.session_state.step = 0
        if 'user_id' not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
        if 'title' not in st.session_state:
            st.session_state.title = "Evoluation niveau Python"
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'answers_list' not in st.session_state:
            st.session_state.answers_list = []
        if 'level' not in st.session_state:
            st.session_state.level = ""
        if 'question_list' not in st.session_state:
            st.session_state.question_list = self.get_questions()
        self.col1, self.col2 = st.columns(2, gap="medium")

    def load_questions(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        return data
    
    # Randomize questions by difficulty
    def randomize_questions_by_difficulty(self, quiz):
        easy_questions = []
        medium_questions = []
        hard_questions = []
        for question in quiz:
            if question["difficulty"] == "Easy":
                easy_questions.append(question)
            elif question["difficulty"] == "Intermediate":
                medium_questions.append(question)
            elif question["difficulty"] == "Hard":
                hard_questions.append(question)

        # Extract the questions from the original data
        good_easy_questions = [
            question for question in easy_questions[0]['questions']]
        good_medium_questions = [
            question for question in medium_questions[0]['questions']]
        good_hard_questions = [
            question for question in hard_questions[0]['questions']]   

        # get 2 random questions from each list
        random_easy_questions = random.sample(good_easy_questions, 2)
        random_medium_questions = random.sample(good_medium_questions, 2)
        random_hard_questions = random.sample(good_hard_questions, 2)

        # combine all 6 questions into one list
        random_questions = random_easy_questions + \
            random_medium_questions + random_hard_questions
        # randomize the order of the questions
        random.shuffle(random_questions)
        return random_questions

    def get_questions(self):
        file_path = "quiz.json"
        quiz = self.load_questions(file_path)
        rand_questions = self.randomize_questions_by_difficulty(quiz)
        return rand_questions

    def prev_step(self):
        if st.session_state.step > 0:
            st.session_state.step -= 1

    def next_step(self):
        if st.session_state.step >= 0 or st.session_state.step <= 8:
            st.session_state.step += 1
    
    def back_to_menu(self):
        st.session_state.step = 0

    def compose_question(self, question, id):
        try:
            st.code(question['code'])
        except:
            pass
        
        try:
            value = st.radio(f"{ id } . { question['prompt'] }!", question['options'])
        except:
            st.write(question)
            value = " "
        return value
    
    def compose_answer(self, id, answer, question):
        st.session_state.answers_list.append({
            "id": id,
            "score": st.session_state.score,
            "user_answer": answer,
            "true_answer": question['answer']
        })
        # call the function to increase the score
        self.increase_score(answer, question, st.session_state.score)

    def increase_score(self, answer, question, score):
        # check in the session state if the answer is correct
        if answer == question['answer']:
            st.session_state.score += question['points']
        else:
            st.session_state.score += 0

    def window(self):
        st.title = st.session_state.title

        if st.session_state.step == 0:
            st.write("# Bienvenue au test d'évaluation des aptitudes en python 👋")
            st.markdown(
                """
                ### Ce test est composé de :red[6 questions] permettant d’évaluer votre niveau en python
                ### Pour commencer, cliquer sur le bouton :blue[Commencer] ci-dessous
                ### La liste de questions est optimisée pour être pratique à remplir.
                ### Pour chaque question, cocher votre réponse puis cliquer sur :blue[Suivant]

                Les plus rapide mettent 1 minute pour répondre aux questions 👈 
                
                :red[En passant à la page suivante, je confirme que j'ai lu et accepté les conditions d\'utilisation]

            """
            )
            st.button("Commencer", on_click=self.next_step)

        elif st.session_state.step == 1:
            st.write("## Commençons par saisir notre classe")

            option = st.selectbox(
                'Quel est votre niveau académique actuel ?',
                ('B1 -> Bachelor1', 'B2 -> Bachelor2', 'B3 -> Bachelor3 ', 'M1 -> Mastère1', 'M2 -> Mastère2')
            )

            new_option = option.split('-')[0].split(' ')[0]
            st.session_state.level = new_option


            st.button("Commencer", on_click=self.next_step)

        elif st.session_state.step == 8:
            st.write("# Evaluation terminée! 👋")
            st.write("Votre score est de: ", st.session_state.score)
            data = {
                "user": st.session_state.user_id,
                "answers": st.session_state.answers_list
            }
            st.button("Recommencer", on_click=self.back_to_menu)
            
        else:
            if st.session_state.step > 1:
                with self.col1:
                    st.button('Précédent', on_click=self.prev_step)

                if st.session_state.step == 8:
                    with self.col2:
                        st.button('Suivant', disabled=True)
                else:
                    with self.col2:
                        st.button('Suivant', on_click=self.next_step)

                if st.session_state.step == 2:
                    answer = self.compose_question(st.session_state.question_list[0], 1)
                    self.compose_answer((0 + 1), answer, st.session_state.question_list[0])
                elif st.session_state.step == 3:
                    answer = self.compose_question(st.session_state.question_list[1], 2)
                    self.compose_answer((1 + 1), answer, st.session_state.question_list[1])
                elif st.session_state.step == 4:
                    answer = self.compose_question(st.session_state.question_list[2], 3)
                    self.compose_answer((2 + 1), answer, st.session_state.question_list[2])
                elif st.session_state.step == 5:
                    answer = self.compose_question(st.session_state.question_list[3], 4)
                    self.compose_answer((3 + 1), answer, st.session_state.question_list[3])
                elif st.session_state.step == 6:
                    answer = self.compose_question(st.session_state.question_list[4], 5)
                    self.compose_answer((4 + 1), answer, st.session_state.question_list[4])
                elif st.session_state.step == 7:
                    answer = self.compose_question(st.session_state.question_list[5], 6)
                    self.compose_answer((5 + 1), answer, st.session_state.question_list[5])


if __name__ == '__main__':
    app = Appraisal()
    app.window()
