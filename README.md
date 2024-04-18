 
# Ai_chatbot
 Create an AI chat bot to answer the query of the users coming to purchase courses on any ed-tech website.

 
<img width="1440" alt="Screenshot 2024-04-17 at 2 07 59 PM" src="https://github.com/agrahjain786/Ai_chatbot/assets/131575356/a0619983-b59a-4d9d-abf4-26a827c9b546">



## Here’s my solution:-

<br>

### Dataset Used:-
I have Used the Udacity Courses Dataset. As This dataset contains over 250+ courses along with the information such as course titles, descriptions, durations, prerequisites, and 12 columns.I have used 950+ FAQ Questions and answers extracted from this dataset to train the chatbot

<br>

### Login Authentications:-
1. Implemented Google SSO OAuth 2.0 that allows users/clients to login into the website and use the chatbot.
 
   <img width="1440" alt="Screenshot 2024-04-17 at 12 20 20 AM" src="https://github.com/agrahjain786/Ai_chatbot/assets/131575356/37179c61-def2-486d-a125-48d3100523e8"><br>


2. Django-Allauth Authentication that allows Doubt Assistant to login and solve the doubts of the users (Only Admin can make the ID-PASS so that only Authorised doubt assistants can access the Doubt Assistant webpage to solve the queries).

   <img width="1440" alt="Screenshot 2024-04-17 at 2 09 26 PM" src="https://github.com/agrahjain786/Ai_chatbot/assets/131575356/7ab5e1e2-1c95-4b19-9e4a-e1d9bb91e0c8"><br>


<br>

### FAQ Integration:-
Integrate a database of 950+ frequently asked questions (FAQs) related to courses. Whenever the query encounters the chatbot retrieve relevant answers from the FAQ database to respond to user queries.
If a new query has been asked by the user then pass it to the doubt assistant and add it to the FAQ list along with the response passed by the Doubt Assistant. So that it can be used for query resolution later if a similar query is asked. 

<img width="1440" alt="Screenshot 2024-04-17 at 2 36 44 PM" src="https://github.com/agrahjain786/Ai_chatbot/assets/131575356/ede97f20-0827-409d-84e5-1d641f12a994"><br>

<br>

### Chatbot Training and Response:-
Uses NLP techniques like NLTK to preprocess the both FAQ dataset and user input query and performs Tokenization, Lemmatisation, removal of punctuation words and stop words with the help of punkt, wordnet, stopwords to generate the tokens.
Uses Scikit-learn to perform TFIDF and Cosine Similarity to make tokens to numbers which helps in retrieve the most relevant answers from the Database.<br>

<br>

### Fallback Mechanism:-
Implemented a mechanism where if a user is not satisfied with the response generated by chatbot even after multiple tries or cosine similarity is zero then the chatbot will fallback to a doubt assistant for further assistance. And add the query and response into the FAQ dataset.<br>

<br>

### Doubt Assistant Webpage:-
Where the authorised doubt assistant encounters the Doubts one by one along with the chat history of the user to give the most statisfied and relevant answer to the user. Doubt Assistant generate the response then after 3 second he/she encounters the new user doubt. And if there is no query in the queue then the webpage automatically reloads in every 5 seconds to refresh and see if any doubt comes or not.
Implemented a feature in which if the user query sends to the Doubt assistant then system checks for 90 seconds to get the response of the query which is done with the help of Database Pooling

<img width="1440" alt="Screenshot 2024-04-17 at 2 28 09 PM" src="https://github.com/agrahjain786/Ai_chatbot/assets/131575356/314ace86-5667-4b3d-b909-9fecae89a5f1"><br>

<br>

### User Satisfaction Feedback:-
Asked the user to submit the feedback/rating after resolving the user query and store the feedback in the Feedback_rating database.
If the user is satisfied then appears the thanks message and end the chat session and if user is not staffed then asked the user for the further assistance.

<img width="1440" alt="Screenshot 2024-04-17 at 2 29 48 PM" src="https://github.com/agrahjain786/Ai_chatbot/assets/131575356/1e53eaf0-8c7f-4c0b-a743-14f6ab44277b"><br>

<br>

### Sharing Data with the sales team:-
Download the Chat Database which contains all the history of all users in the form of CSV file. And this file can only downloaded by Admin or the Authorised users of the Sales team.

<img width="1440" alt="Screenshot 2024-04-17 at 2 31 34 PM" src="https://github.com/agrahjain786/Ai_chatbot/assets/131575356/19d93762-0878-4977-9792-e03c401d2340"><br>

<br>

### Performance Monitoring:-
Implement monitors to track the efficiency and effectiveness of the chat bot like total time taken by the chatbot to generate the response, fallback rates, number of times a query is asked in the conversation, feedback of each responses. This data is also downloaded by the Admin only and the Authorised People which Admins allows in the form of CSV file. 

<img width="1440" alt="Screenshot 2024-04-17 at 2 32 48 PM" src="https://github.com/agrahjain786/Ai_chatbot/assets/131575356/a7f293cc-3a08-4c66-9643-3e4a14138046"><br>


