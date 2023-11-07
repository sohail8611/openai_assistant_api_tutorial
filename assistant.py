from openai import OpenAI
import json
import time
client = OpenAI()


theUser = "maxi"
theUserInput = """
Solve the following system of equations using gauss elimination, use code interpreter.:
-7x+-4y-+10z = 1
-5x + 10y -2z = -19
5x +2y -7z = 3
"""


# Read the contents of the user.json file
with open('user.json', 'r') as file:
    user_data = json.load(file)



for i in user_data:
    if i['username'] == theUser and len(i['thread'])<1:
        thread = client.beta.threads.create()
        i['thread'] = thread.id
        with open('user.json', 'w') as file:
            json.dump(user_data, file, indent=4)
        break



with open('user.json', 'r') as file:
    user_data = json.load(file)

activeUserThreadId = ""
for i in user_data:
    if i['username'] == theUser:
        activeUserThreadId = i['thread']

message = client.beta.threads.messages.create(
    thread_id=activeUserThreadId,
    role="user",
    content=theUserInput
)


run = client.beta.threads.runs.create(
  thread_id=activeUserThreadId,
  assistant_id="asst_vlA8xuDYfpVJnRBcP0xWplxP",
  instructions=f"Please address the user as {theUser} including the response."
)
# print(run)
while True:
    time.sleep(2)
    run = client.beta.threads.runs.retrieve(
    thread_id=activeUserThreadId,
    run_id=run.id
    )
    if run.status =='completed':
        break
    else:
        pass

messages = client.beta.threads.messages.list(
  thread_id=activeUserThreadId
)


print(f'{theUser} : {theUserInput}')
print(f'Assistant: {messages.data[0].content[0].text.value}')



        



