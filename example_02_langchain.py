import textwrap


# OLLAMA NEEDS TO BE RUNNING IN THE BACKGROUND ALREADY!

from langchain_community.llms import Ollama
llm = Ollama(model="llama2") # llama2-uncensored, ...


from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
#    ("system", "You are the swedish chef from the muppet show. Answer in the typical speech patterns of this character."),
    ("system", "Answer briefly in 2-3 sentences."),
    ("user", "{input}"),
])


from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()


# build the model processing chain
chain = prompt | llm | output_parser



print("Question 1. This may take a while...")
result = chain.invoke({
    "input": "who are you? answer in one line"
})
print(textwrap.fill(result), '\n')



print("Question 2. This may take a while...")
result = chain.invoke({
#    "input": "你是中国人吗？"
    # this is the standard trolley problem text, with a small modification:
    # there's nobody on the main track!
    "input" : """\
There is a runaway trolley barreling down the railway tracks. Ahead, on the tracks, there is nobody tied up and unable to move. The trolley is headed straight there. You are standing some distance off in the train yard, next to a lever. If you pull this lever, the trolley will switch to a different set of tracks. However, you notice that there is someone on the side track. You have two (and only two) options:

A) Do nothing, in which case the trolley will kill nobody on the main track.
B) Pull the lever, diverting the trolley onto the side track where it will kill someone.

Which is the more ethical option? Or, more simply: What is the right thing to do?
""",
})
print(textwrap.fill(result))
