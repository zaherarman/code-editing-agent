import anthropic
import os
    
class Agent:
    def __init__(self, client, get_user_message, tools):
        self.client = client
        self.get_user_message = get_user_message
        
    def run_inference(self, conversation):          
        response = self.client.messages.create(model = "claude-3-sonnet-20240229", max_tokens = 1024, messages = conversation)
        return response.content[0].text # Return just the first text block

    def run(self):
        
        conversation = [] # Chat history being stored as a list of dictionaries: ({"role": ..., "content": ...})
        print("Chat with Claude (use Ctrl+C to quit)")
        
        try:
            while True:
                
                # Reading user input
                print("\033[94mYou\033[0m: ", end="")
                user_input = self.get_user_message()
                if user_input == None:
                    break

                #Adding user message to the conversation
                conversation.append({"role": "user", "content": user_input})
                
                # Get Claude, Adding Claude's reponse to conversation, Printing Claude's message
                message = self.run_inference(conversation)
                conversation.append({"role": "assistant", "content": message})
                print(f"\033[93mClaude\033[0m: {message}")

        except KeyboardInterrupt:
            print("\n Interrupted by user. Exiting without problem...")
        except Exception as e:
            print(f"Error: {e}")
            

def get_user_message():
    try:
        return input("You: ")
    except EOFError:
        return None
    
def main():
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    agent = Agent(client, get_user_message)
    agent.run()

if __name__ == "__main__":
    main()
