# import anthropic
# import os
# import dataclasses
# import json
# import typing
# import re

# class ToolDefinition:
#     name: str
#     description: str
#     input_schema:dict # Json schema
#     function: typing.Callable[[dict], str]
    
# class Agent:
#     def __init__(self, client, get_user_message, tools):
#         self.client = client
#         self.get_user_message = get_user_message
#         self.tools = tools
        
#     def run_inference(self, conversation):
#         anthropic_tools = []
        
#         for tool in self.tools:
#             anthropic_tools.append({"name": tool.name, "description": tool.description, "input_schema": tool.input_schema})
            
#         response = self.client.messages.create(model = "claude-3-sonnet-20240229", max_tokens = 1024, messages = conversation, tools = anthropic_tools)
#         return response.content[0].text # Return just the first text block

#     def run(self):
        
#         conversation = [] # Chat history being stored as a list of dictionaries: ({"role": ..., "content": ...})
#         print("Chat with Claude (use Ctrl+C to quit)")
        
#         try:
#             while True:
                
#                 # Reading user input
#                 print("\033[94mYou\033[0m: ", end="")
#                 user_input = self.get_user_message()
#                 if user_input == None:
#                     break

#                 #Adding user message to the conversation
#                 conversation.append({"role": "user", "content": user_input})
                
#                 # Get Claude, Adding Claude's reponse to conversation, Printing Claude's message
#                 message = self.run_inference(conversation)
#                 conversation.append({"role": "assistant", "content": message})
#                 print(f"\033[93mClaude\033[0m: {message}")

#                 # Check if Claude asked to use a tool
#                 # We expect something like: `read_file({"path": "/foo/bar.txt"})`

#                 m = re.search(r"(\w+)\((\{.*\})\)", message)
#                 if m:
#                     tool_name, raw_args = m.group(1), m.group(2)
#                     for tool in self.tools:
#                         if tool.name == tool_name:
#                             args = json.loads(raw_args)
#                             result = tool.function(args)
                            
#                             # Inject the result aback into the convo
#                             result_msg = f"RESULT {tool_name}: {result}"
#                             conversation.append({"role": "tool", "content": result_msg})
#                             print(f"\033[95m[tool {tool_name}]\033[0m {result}")

#                             # Ask Claude again with the new info
#                             followup = self.run_inference(conversation)
#                             conversation.append({"role": "assistant", "content": followup})
#                             print(f"\033[93mClaude\033[0m: {followup}")
#                             break                            
                
#         except KeyboardInterrupt:
#             print("\n Interrupted by user. Exiting without problem...")
#         except Exception as e:
#             print(f"Error: {e}")
            

# def get_user_message():
#     try:
#         return input("You: ")
#     except EOFError:
#         return None

# def read_file_tool(args: dict) -> str:
#     path = args.net("path")
#     try:
#         with open(path, "r") as f:
#             return f.read()
#     except Exception as e:
#         return f"Error reading '{path}': {e}"
    
# def main():
#     client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
#     tools = [
#         ToolDefinition(
#             name="read_file",
#             description="Read the contents of a text file at the given path.",
#             input_schema={
#                 "type": "object",
#                 "properties": {
#                     "path": {"type": "string", "description": "Filesystem path to read"},
#                 },
#                 "required": ["path"],
#             },
#             function=read_file_tool,
#         ),
#         # Add more tools here
#     ]
    
#     agent = Agent(client, get_user_message)
#     agent.run()

# if __name__ == "__main__":
#     main()
