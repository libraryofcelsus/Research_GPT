import sys
sys.path.insert(0, './scripts')
sys.path.insert(0, './config')
import os
import openai
import time
from time import time, sleep
import datetime
from uuid import uuid4
import concurrent.futures


def chatgpt200_completion(messages, model="gpt-3.5-turbo", temp=0.2):
    max_retry = 7
    retry = 0
    while  True:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=200)
            text = response['choices'][0]['message']['content']
            temperature = temp
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                print(f"Exiting due to an error in ChatGPT: {oops}")
                exit(1)
            print(f'Error communicating with OpenAI: "{oops}" - Retrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)
            
           
def chatgpt250_completion(messages, model="gpt-3.5-turbo", temp=0.40):
    max_retry = 7
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=250)
            text = response['choices'][0]['message']['content']
            temperature = temp
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                print(f"Exiting due to an error in ChatGPT: {oops}")
                exit(1)
            print(f'Error communicating with OpenAI: "{oops}" - Retrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)
            
            
def chatgpt35_completion(messages, model="gpt-3.5-turbo", temp=0.3):
    max_retry = 7
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages)
            text = response['choices'][0]['message']['content']
            temperature = temp
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                print(f"Exiting due to an error in ChatGPT: {oops}")
                exit(1)
            print(f'Error communicating with OpenAI: "{oops}" - Retrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)
            
            
def chatgpt_tasklist_completion(messages, model="gpt-4", temp=0.3):
    max_retry = 7
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages)
            text = response['choices'][0]['message']['content']
            temperature = temp
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                print(f"Exiting due to an error in ChatGPT: {oops}")
                exit(1)
            print(f'Error communicating with OpenAI: "{oops}" - Retrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
        
        
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


if __name__ == '__main__':
    openai.api_key = open_file('key_openai.txt')
    conversation = list()
    int_conversation = list()
    conversation2 = list()
    tasklist_completion = list()
    master_tasklist = list()
    tasklist = list()
    tasklist_log = list()
    counter = 0
    if not os.path.exists('logs/complete_chat_logs'):
        os.makedirs('logs/complete_chat_logs')
    bot_name = open_file('./config/prompt_bot_name.txt')
    username = open_file('./config/prompt_username.txt')
    main_prompt = open_file('./config/prompt_main.txt').replace('<<NAME>>', bot_name)
    greeting_msg = open_file('./config/prompt_greeting.txt').replace('<<NAME>>', bot_name)
    while True:
        # # Get Timestamp
        timestamp = time()
        # # Start or Continue Conversation based on if response exists
        conversation.append({'role': 'system', 'content': '%s' % main_prompt})
        int_conversation.append({'role': 'system', 'content': '%s' % main_prompt})
        conversation.append({'role': 'assistant', 'content': "%s" % greeting_msg})
        print("\n%s" % greeting_msg)
        # # User Input Text
        a = input(f'\n\nUSER: ')
        message_input = a
        conversation.append({'role': 'user', 'content': a})        
        # # Generate Semantic Search Terms
        tasklist.append({'role': 'system', 'content': "You are a task coordinator. Your job is to take user input and create a list of 2-5 inquiries to be used for a semantic database search of a chatbot's memories. Use the format [- 'INQUIRY']."})
        tasklist.append({'role': 'user', 'content': "USER INQUIRY: %s" % a})
        tasklist.append({'role': 'assistant', 'content': "List of Semantic Search Terms: "})
        tasklist_output = chatgpt200_completion(tasklist)
    #    print(tasklist_output)

       # # # Inner Monologue Generation
        conversation.append({'role': 'assistant', 'content': "Other possible user meanings: %s" % tasklist_output})
        conversation.append({'role': 'assistant', 'content': "USER MESSAGE: %s;\nBased on the user, %s's message, compose a brief silent soliloquy as an inner monologue that reflects on your deepest contemplations in relation to the user's message.\n\nINNER_MONOLOGUE: " % (a, username)})
        output_one = chatgpt250_completion(conversation)
        message = output_one
        print('\n\nINNER_MONOLOGUE: %s' % output_one)
        output_log = f'\nUSER: {a}\n\n{bot_name}: {output_one}'
        # # Clear Conversation List
        conversation.clear()
        # # Memory DB Search
        # # Intuition Generation
        int_conversation.append({'role': 'assistant', 'content': "%s" % greeting_msg})
        int_conversation.append({'role': 'user', 'content': tasklist_output})
        int_conversation.append({'role': 'assistant', 'content': "INNER MONOLOGUE: %s;\n\nUSER MESSAGE: %s;\nIn a single paragraph, interpret the user, %s's message in third person by creating an intuitive plan on what information needs to be researched, even if the user is uncertain about their own needs.;\nINTUITION: " % (output_one, a, username)})
        output_two = chatgpt200_completion(int_conversation)
        message_two = output_two
        print('\n\nINTUITION: %s' % output_two)
        output_two_log = f'\nUSER: {a}\n\n{bot_name}: {output_two}'
        # # Test for basic Autonomous Tasklist Generation and Task Completion
        master_tasklist.append({'role': 'system', 'content': "You are a stateless task list coordinator. Your job is to take the user's input and transform it into a list of independent research queries that can be executed by separate AI agents in a cluster computing environment. The other asynchronous Ai agents are also stateless and cannot communicate with each other or the user during task execution. Exclude tasks involving final product production, hallucinations, user communication, or checking work with other agents. Respond using the following format: '- [task]'"})
        master_tasklist.append({'role': 'user', 'content': "USER FACING CHATBOT'S INTUITIVE ACTION PLAN:\n%s" % output_two})
        master_tasklist.append({'role': 'user', 'content': "USER INQUIRY:\n%s" % a})
        master_tasklist.append({'role': 'user', 'content': "SEMANTICALLY SIMILAR INQUIRIES:\n%s" % tasklist_output})
        master_tasklist.append({'role': 'assistant', 'content': "TASK LIST:"})
        master_tasklist_output = chatgpt_tasklist_completion(master_tasklist)
        print(master_tasklist_output)
        tasklist_completion.append({'role': 'system', 'content': "You are the final response module of a cluster compute Ai-Chatbot. Your job is to take the completed task list, and give a verbose response to the end user in accordance with their initial request."})
        tasklist_completion.append({'role': 'user', 'content': "%s" % master_tasklist_output})
        task = {}
        task_result = {}
        task_result2 = {}
        task_counter = 1
        # # Split bullet points into separate lines to be used as individual queries
        lines = master_tasklist_output.splitlines()
        print('\n\nSYSTEM: Would you like to autonomously complete this task list?\n        Press Y for yes or N for no.')
        user_input = input("'Y' or 'N': ")
        if user_input == 'y':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(
                        lambda line, task_counter, conversation, tasklist_completion: (
                            tasklist_completion.append({'role': 'user', 'content': "ASSIGNED TASK:\n%s" % line}),
                            conversation.append({'role': 'system', 'content': "You are a sub-module for an Autonomous Ai-Chatbot. You are one of many agents in a chain. You are to take the given task and complete it in its entirety. Take other tasks into account when formulating your answer."}),
                            conversation.append({'role': 'user', 'content': "Task list:\n%s" % master_tasklist_output}),
                            conversation.append({'role': 'assistant', 'content': "Bot %s: I have studied the given tasklist.  What is my assigned task?" % task_counter}),
                            conversation.append({'role': 'user', 'content': "Bot %s's Assigned task: %s" % (task_counter, line)}),
                            conversation.append({'role': 'assistant', 'content': "Bot %s:" % task_counter}),
                            task_completion := chatgpt35_completion(conversation),
                            conversation.clear(),
                            tasklist_completion.append({'role': 'assistant', 'content': "COMPLETED TASK:\n%s" % task_completion}),
                            tasklist_log.append({'role': 'user', 'content': "ASSIGNED TASK:\n%s" % line}),
                            tasklist_log.append({'role': 'assistant', 'content': "COMPLETED TASK:\n%s" % task_completion}),
                            print(line),
                            print(task_completion),
                        ) if line != "None" else tasklist_completion,
                        line, task_counter, conversation.copy(), []
                    )
                    for task_counter, line in enumerate(lines)
                ]
            tasklist_completion.append({'role': 'user', 'content': "Take the given set of tasks and completed responses and transmute them into a verbose response for the end user in accordance with their request. The end user is both unaware and unable to see any of your research. User's initial request: %s" % a})
            print('\n\nGenerating Final Output...')
            final_response_complete = chatgpt_tasklist_completion(tasklist_completion)
            print('\nFINAL OUTPUT:\n%s' % final_response_complete)
            complete_message = f'\nUSER: {a}\n\nINNER_MONOLOGUE: {output_one}\n\nINTUITION: {output_two}\n\n{bot_name}: {tasklist_log}\n\nFINAL OUTPUT: {final_response_complete}'
            filename = '%s_chat.txt' % timestamp
            save_file('logs/complete_chat_logs/%s' % filename, complete_message)
            conversation.clear()
            int_conversation.clear()
            conversation2.clear()
            tasklist_completion.clear()
            master_tasklist.clear()
            tasklist.clear()
            tasklist_log.clear()
        continue
