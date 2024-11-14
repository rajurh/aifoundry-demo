

# create and run a thread with a message
thread = project.agents.create_thread() 
message = project.agents.create_message( 
    thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?" 
) 
run = project.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id) 
if run.status == "failed": 
    print(f"Run failed: {run.last_error}") 
    exit()

# get messages from the thread and print the response (last message)
messages = project.agents.list_messages(thread_id=thread.id) 
print(f"Response: {messages[-1]}") 
