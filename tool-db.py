# load the llm
from llama_cpp import Llama
# https://huggingface.co/pankajmathur/orca_mini_3b
llm = Llama(model_path=r"C:\Users\root\Documents\tiny_tools\orca-mini-3b.ggmlv3.q4_0.bin", n_gpu_layers=0)
llm.verbose = False

# we are using loopGPT's tool documentation here
# as it saves writing strings over and over
# https://github.com/farizrahman4u/loopgpt
import loopgpt.tools as tools 

# create in memory vector DB
import chromadb
client = chromadb.Client()
collection = client.create_collection("tools")

# add tool embedding vectors to database
for i, tool in enumerate(tools.builtin_tools()) :
    tool = tool()
    print(f"adding {tool.id} to db")
    collection.add(
        documents=tool.__doc__.split('\n')[0],
        metadatas={'name' : tool.id},
        ids = str(i)
    )

prompt_template = """Below is some text about your current objective. Your task is to analyse this text and come up with a description of a computer program or software to complete that objective.

objective: {objective}

The program or tool needed to complete this task should"""

# this loop asks the user to enter a task
while True:
    # generate completion for an input task
    goal = input('task: ')
    prompt = prompt_template.format(objective = goal)
    response = llm(prompt, stop='.')
    
    # take the response and print it
    response = response['choices'][0]['text']
    print("model is looking for:", *response.splitlines(), sep = '\n\t')

    # query the database for similar tools
    results = collection.query(
        query_texts=[*response.split('\n')],
        n_results=3
    )

    # print the top 3 most useful tools, usually directly calling the top one is best
    # but this would allow for the LLM to perform evaluation and pick the best tool
    # if you have dense clusters in the latent space
    for id in results['ids'][0] :
       print(tools.builtin_tools()[int(id)]().id)