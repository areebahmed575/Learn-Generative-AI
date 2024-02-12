from openai.types.beta.threads import Run
from openai.types.beta.thread import Thread
from openai.types.beta.assistant import Assistant

from openai.types.beta.assistant_create_params import Tool
import time
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from typing import Literal
import os
from functions import available_functions


 

_: bool = load_dotenv(find_dotenv()) 

client: OpenAI = OpenAI()


class Trip:
    def __init__(self, model: str = "gpt-3.5-turbo-1106"):
        self.client = OpenAI()
        self.model = model
        self.assistant: Assistant | None = None
        self.thread: Thread | None = None
        self.run: Run | None = None


    def list_assistant(self):
        assistant_list = self.client.beta.assistants.list()
        assistant_list_json = assistant_list.model_dump
        return assistant_list_json['data'] if "data" in assistant_list_json else []
    

    def update_existing_assistant(self,assistant_id: str, new_instructions: str, tools: list, file_obj: list[str]):
        self.assistant = self.client.beta.assistants.update(
            assistant_id=assistant_id,
            instructions=new_instructions,  
            tools=tools,
            file=file_obj,
        ) 
        return self.assistant

    def find_and_set_assistant(self,name: str, instructions: str, tools: list[Tool], file_obj: list[str]):

        assistant_list = self.list_assistant()
        print("Retrieved assistants list...")
        if self.assistant is not None:
            
           for assistant in assistant_list:
                if assistant["name"] == name:
                    print("Found assistant...",  assistant['name'] == name)
                    print("Existing Assitant ID", assistant['id'])
                    self.update_existing_assistant(assistant_id=assistant['id'], 
                                                   new_instructions=name, 
                                                   tools=tools, 
                                                   file_obj=file_obj
                                                   )

                    break
    


    def create_assistant(self, name: str, instructions: str, tools: list, file_obj: list[str], model: str = "gpt-3.5-turbo-1106")-> Assistant:

        self.find_and_set_assistant(name=name, 
                                    instructions=instructions,
                                    tools=tools, 
                                    file_obj=[])
        if self.assistant is None :
            print("Creating an assitant")
            self.assistant = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=model

            ) 
            return self.assistant   
        
    def create_thread(self)-> Thread:
            self.client.beta.threads.create()
            return self.thread   
            

    def add_message_to_thread(self,role:Literal['user'], content: str):
         if self.thread is not None:
            raise ValueError("Thread is not set")
         self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content
         )

    def create_run(self,instructions:str)-> Run:
         
         if self.assistant is None:
            raise ValueError("Assistant is not set")
         
         if self.thread is None:
             raise ValueError("Thread is not set")
         
         self.run=self.client.beta.runs.create(
              thread_id=self.thread.id,
              assistant_id=self.assistant.id,
              instructions=instructions
         )
         return self.run
    
    
    
    def show_json(message, obj):
        print(message, json.loads(obj.model_dump_json()))

    def messages(self):
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id)
        return messages    


    def get_run_result(self,run: Run, thread: Thread):
        if self.run is None:
            raise ValueError("Run is not set")
        
        while run.status == ["completed","failed"]:
            run_status= client.beta.threads.runs.retrieve(thread_id=self.thread.id,run_id=self.run.id)
            # Add run steps retrieval here for debuging
            run_steps = self.client.beta.threads.runs.steps.list(thread_id=self.thread.id, run_id=self.run.id)
            self.show_json("Run Steps:", run_steps)
            print(run_status.status ,'.....')
            time.sleep(4)
            if run_status.status == 'completed':
                processed_response = self.process_messages()
                return processed_response
            elif run_status.status == 'requires_action' and run_status.required_action is not None:
                print("Function Calling ...")
                #st.sidebar.write(f"Function Calling ...")
                self.call_required_functions(
                    run_status.required_action.submit_tool_outputs.model_dump())
            elif run.status == "failed":
                print("Run failed.")
                break
            else:
                print(f"Waiting for the Assistant to process...: {run.status}")


    def call_required_functions(self, action_required):
        tool_outputs = []
        print("Calling tool call required functions...",action_required["tool_calls"])
        
        
        for action in action_required["tool_calls"]:  
            function_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])
            print('function_name', function_name)
            print('function_arguments', arguments)

            #st.sidebar.write(f"Calling {function_name} with:")
            for key, value in arguments.items():
                st.sidebar.write(f"{key}: {value}")


            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                output = function_to_call(**arguments)
                tool_outputs.append({
                    "id":action['id'], 
                    "output":output
                })    
            else:
                #st.sidebar.write(f"Unknown function: {function_name}")
                st.stop()
                raise ValueError(f"Unknown function: {function_name}")
            

        print("Submitting outputs back to the Assistant...")
        #st.sidebar.write("Submitting outputs back to the Assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=self.run.id,
            tool_outputs=tool_outputs
        )    
 
             



            














              






