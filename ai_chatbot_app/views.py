from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Chat,FAQ,Doubt,ChatMonitor,feedback_rating as feedback
from django.utils import timezone
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import time
import logging
import random

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
query_count = defaultdict(int)
ai_or_assistant = 0
logger = logging.getLogger(__name__)


# Create your views here.


greeting_responses = ["Hello! Welcome to our ed-tech platform. How can I assist you today?",
                      "Hi there! How can I help you with your course purchase?",
                      "Welcome! How can I assist you in finding the perfect course?"]

normal_responses = ["Anything i call help you with?"]

help_responses = ["How can I assist you today?",
                  "What do you need help with?",
                  "I'm here to help. What can I do for you?"]

goodbye_responses = ["Thank you for visiting our platform! Have a great day!",
                     "It was a pleasure assisting you. Have a wonderful day!",
                     "Goodbye! If you have any further questions, feel free to ask."]


def submit_feedback(request, user_query):
    if request.method == 'POST':
        rating = int(user_query)
        new_feedback = feedback(user=request.user, rating=rating, message='Feedback', response='feddback')
        new_feedback.save()
        if rating > 3:
            reply = 'Thank you for your feedback. We are glad you liked our service.'
        else:
            reply = 'Thank you for your feedback. We will try to improve our service. If anything we can assist you more?.'
    return reply


def doubt_assistant(request):
    doubts = Doubt.objects.filter(answer='')
    if  request.method == 'POST':
        answer = request.POST.get('message')
        doubt = doubts[0]
        doubt.answer = answer
        doubt.solved_doubt_at = timezone.now()
        new_faq = FAQ(question=doubt.query, answer=answer)
        new_faq.save()
        doubt.save()
        doubts = Doubt.objects.filter(answer='')
        
    if len(doubts) > 0:
        doubt = doubts[0]
        chats = Chat.objects.filter(user=doubt.user)
    else:
        chats = []
    return render(request, 'ai_chatbot_app/doubt_assistant.html' , {'doubts': doubts , 'chats': chats})



def save_doubt(request,user_query):
    new_query = Doubt(user=request.user, query=user_query, created_at=timezone.now(), answer='', solved_doubt_at=None)
    new_query.save()
    
    

def doubt_assistant_available(request, user_query):
    save_doubt(request, user_query)
    global ai_or_assistant
    start_time = time.time()
    response = ''
    while True:
        row = Doubt.objects.filter(user=request.user, query=user_query).last()
        if row.answer != '':
            ai_or_assistant = 1
            response = row.answer
            break
        else:
            time.sleep(1)
            
        if time.time() - start_time > 90:
            response = 'Sorry, No Doubt assistant available right now. Please try again later.'
            break
    return response



def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stopwords.words('english')]
    return ' '.join(tokens)



def generate_response(request, user_query, all_faqs):
    if any(num in user_query for num in ["1", "2", "3", "4", "5"]):
        return submit_feedback(request,user_query)
    query = user_query.lower()
    if any(greeting in query for greeting in ["hello", "hi", "hey" ]):
        return random.choice(greeting_responses)
    elif any(payment in query for payment in ["yes","okay", "ok"]):
        return random.choice(normal_responses)
    elif any(help_word in query for help_word in ["help", "assist", "support"]):
        return random.choice(help_responses)
    elif any(goodbye_word in query for goodbye_word in ["bye", "goodbye","exit","quit"]):
        return random.choice(goodbye_responses)
    else:
        all_faqs = [(faq, preprocess_text(faq.question)) for faq in all_faqs]
        processed_query = preprocess_text(user_query)

        vectorizer = TfidfVectorizer().fit_transform([processed_query] + [faq[1] for faq in all_faqs])
        cosine_similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
        most_similar_faq_index = cosine_similarities.argmax()

        if cosine_similarities[most_similar_faq_index] == 0:
            response = doubt_assistant_available(request, user_query)
            
        else:
            response = all_faqs[most_similar_faq_index][0].answer
        
        query_count[user_query] += 1
        
        if query_count[user_query] > 3:
            response = doubt_assistant_available(request, user_query)
            
        return response
    


def home(request):
    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        data_type = request.POST.get('type')
        print(data_type)
        if data_type == 'message':
            start_time = time.time()
            message = request.POST.get('message')
            response = generate_response(request, message, FAQ.objects.all())
            end_time = time.time()
            response_time = (end_time - start_time)
            logger.info(f'User input: {message}, Chatbot response: {response}, Response time: {response_time}')
            
            if request.user.is_authenticated:
                chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
                chat.save()
                chatmonitor = ChatMonitor(user=request.user, message=message, response=response, response_time=response_time, fallback=ai_or_assistant)
                chatmonitor.save()
                
            return JsonResponse({'message': message, 'response': response, 'ai_or_assistant': ai_or_assistant})
        
        else:
            print(data_type)
            rating = request.POST.get('rating')
            # message = request.POST.get('message')
            # reply = request.POST.get('response')
            response = submit_feedback(request, rating)
            return JsonResponse({'response': response})
    
    if request.user.is_authenticated:
        return render(request, 'ai_chatbot_app/home.html', {'chats': chats})
    else :
        return render(request, 'ai_chatbot_app/home.html')
    
    
    

def doubt_assistant_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            
            if user.groups.filter(name='Doubt Assistants').exists():
                auth.login(request, user)
                return redirect('doubt_assistant')
            else:
                error_message = 'You are not authorized to access the Doubt Assistant'
                return render(request, 'ai_chatbot_app/doubt_assistant_login.html', {'error_message': error_message})
        else:
            error_message = 'Invalid username or password'
            return render(request, 'ai_chatbot_app/doubt_assistant_login.html', {'error_message': error_message})
    else:
        return render(request, 'ai_chatbot_app/doubt_assistant_login.html')
    
    
    
def login(request):
    return render(request, 'ai_chatbot_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('/login/')


def doubt_assistant_logout(request):
    auth.logout(request)
    return redirect('')





