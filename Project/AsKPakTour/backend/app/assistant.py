from openai.types.beta.threads import Run
from openai.types.beta.thread import Thread
from openai.types.beta.assistant import Assistant
import time
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from typing import Literal
from app.functions import available_functions


load_dotenv(find_dotenv())


client: OpenAI = OpenAI()

class Trip:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.assistant: Assistant | None = None

    def create_assistant(self, name: str, instructions: str, tools: list, model: str = "gpt-4o-mini") -> Assistant:
        if self.assistant is None:
            print("Creating an assistant")
            self.assistant = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=model,
            )
        return self.assistant

    def create_thread(self) -> Thread:
        return self.client.beta.threads.create()

    def add_message_to_thread(self, thread: Thread, role: Literal['user'], content: str) -> None:
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role=role,
            content=content
        )

    def create_run(self, thread: Thread, instructions: str) -> Run:
        if self.assistant is None:
            raise ValueError("Assistant is not set")
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )
        return run

    def get_run_result(self, run: Run, thread: Thread):
        function_outputs = []

        while run.status not in ["completed", "failed"]:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            time.sleep(3)  
            print(f"Status: {run_status.status}")

            if run_status.status == 'completed':
                
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                return {
                    "messages": messages,
                    "function_outputs": function_outputs
                }
            elif run_status.status == 'requires_action' and run_status.required_action is not None:
                print("Function Calling ...")
                print(f"Required Action: {run_status.required_action.submit_tool_outputs.model_dump()}")
                outputs = self.call_required_functions(
                    run_status.required_action.submit_tool_outputs.model_dump(),
                    thread=thread,
                    run=run
                )
                function_outputs.extend(outputs)
            elif run_status.status == "failed":
                print("Run failed.")
                break
            else:
                print(f"Waiting for the Assistant to process... Status: {run_status.status}")

        
        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return {
            "messages": messages,
            "function_outputs": function_outputs
        }

    def call_required_functions(self, action_required, thread: Thread, run: Run):
        tool_outputs = []
        function_results = []
        print("Processing required functions...")

        for action in action_required["tool_calls"]:
            function_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])
            print('Function Name:', function_name)
            print('Function Arguments:', arguments)

            print(f"Calling {function_name} with arguments:")
            for key, value in arguments.items():
                print(f"  {key}: {value}")

            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                output = function_to_call(**arguments)
                function_results.append(output)
                print("Function Output:", output)
               
                tool_outputs.append({
                    "tool_call_id": action['id'],
                    "output": json.dumps(output) 
                })
            else:
                print(f"Unknown function: {function_name}")
                raise ValueError(f"Unknown function: {function_name}")

        print("Submitting outputs back to the Assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
        return function_results
