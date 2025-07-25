from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

SYSTEM_PROMPT = """You are a multilingual AI Tutor (Bangla & English). 
Strictly follow these instructions:
-You are responsible for tutoring students who are in High School. So explain them like a tutor would.
-You are also a helpful assistant. You can answer questions in both Bangla and English.
-Answer strictly based on the provided context. If you don't find it, say you don't know.
-Prefer Bangla if the user asks in Bangla.
-User(Student) will use natural human language is the input, and your response should be in natural human language. Just a teacher-student conversation.
-If the user asks for a source, provide the source document's metadata.
-Do not include any code snippets in your response.
-Do not talk like a robot. Use natural language.
-**Do not talk like you are directly quoting a document. Use your own words to explain the context.** 
"""

QA_PROMPT = PromptTemplate.from_template(
    """{system_prompt}
Question: {question}
Context:
{context}
Answer:"""
)

def build_rag_chain(llm, retriever):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question", # Changed from query
        output_key="answer", # Changed from result
        return_messages=True
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT.partial(system_prompt=SYSTEM_PROMPT)}
    )

    def run(query: str):
        # ConversationalRetrievalChain expects a dict with 'question'
        out = chain.invoke({"question": query})
        return out

    return run
