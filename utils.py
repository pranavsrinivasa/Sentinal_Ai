import os 
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex,SummaryIndex,SimpleDirectoryReader
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.core.agent import ReActAgent
from llama_index.llms.groq import Groq
from llama_index.core.tools import QueryEngineTool
from llama_index.core.prompts import ChatMessage

class cyberbot:
    def __init__(self) -> None:

        load_dotenv()
        os.environ['GOOGLE_API_KEY']  = os.getenv('GOOGLE_API_KEY')
        if os.getenv('GOOGLE_API_KEY') != 'YOUR_API_KEY':
            print('API LOADED')
        else:
            print("PLEASE ADD API")
        self.gemma_llm = Gemini(model='models/gemini-1.5-flash',temperature=0.7,max_tokens=200000)
        self.embed_model = embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')
        reader = SimpleDirectoryReader(input_dir="Data")
        self.documents = reader.load_data()
        self.groq_llm = Groq(model="llama3-70b-8192", api_key="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")

        pass

    def create_qe(self):

        
        splitter2 = SentenceSplitter(chunk_size = 2000,chunk_overlap=200)
        nodes2 = splitter2.get_nodes_from_documents(self.documents)

        if not os.path.exists('F:\Devfolio_hack\devfolio_hackathon-Cyber-AI\VectorData'):
            store = VectorStoreIndex(nodes2,embed_model=self.embed_model,show_progress=True)
            store.storage_context.persist(
                persist_dir='F:\Devfolio_hack\devfolio_hackathon-Cyber-AI\VectorData'
            )
        else:
            store = load_index_from_storage(
                            StorageContext.from_defaults(persist_dir=f"F:\Devfolio_hack\devfolio_hackathon-Cyber-AI\VectorData"),
                            embed_model = self.embed_model
                        )
        
        summary_index = SummaryIndex(nodes2)
        self.vqe = store.as_query_engine(llm=self.gemma_llm)
        self.sqe = summary_index.as_query_engine(llm=self.gemma_llm)

        return
    
    def main_agent(self,proompt):
        self.create_qe()
        tools = [QueryEngineTool.from_defaults(name="vector_tool", description="This tool is used to understand specifics about the context",query_engine=self.vqe), QueryEngineTool.from_defaults(query_engine=self.sqe,name="summary_tool",description="This tool provides overall summary about the context")]

        context = """
                Role: CyberSecurity Expert
                Instructions:
                - You are give have the tools vector_tool and summary_tool
                - According to the user query you will either have to create a Cyber Audit Report or provide information about the logs
                - Use the tools to get context and answer the user's query
                - Do not hallucinate context
                - Do not hallucinate user query
                - Do not deviate from the instructions and stick to the role
                - Follow the instructions 
                - Answer in detail to answer the user's query
                - Provide the complete output at the end
                - Provide detailed request as input to the tools
        """

        agent = ReActAgent.from_tools(tools=tools,context=context,llm=self.groq_llm,verbose=True,max_iterations=100)
        res = agent.query(proompt)

        return res.response
    
    def unstruct_to_csv(self,data):
        with open('Data\cybersecurity_logs.txt') as f:
            read_logs = f.read()
        messages = [ChatMessage(role="system",content="""
        Instructions:
        - From the input data, split into relevant columns and provide output as comma seperated values (csv)
        - The relevant columns from the unstructured data need to created
        - The data from unstructured data need to placed under the relevant columns
        - Do no hallucinate the data
        - Do not change the data from the user input
        - Do not hallucinate the columns names
        - Follow strictly the format of comma seperated values
        - Do not deviate from the instructions
        - Follow the instructions strictly
        Example:
        - Eg1:
        Input: Rajesh from 12 to 1 has created a Agentic RAG pilot
                Pranav from 2 to 3 has completed a Cybersecurity analysis
                Akbhar from 11-12 did a development improvement
                John in the span of 1-5 did got Clients on board
        Output: Name,time,work
                Rajesh,12-1,Agentic Rag pilot
                Pranav,2-3,Cybersecurity analysis
                Akbhar,11-12,Development
                John,1-5, Client Onboarding
        - Eg2: 
        Input:2024-09-22 15:09 Rs134 Rs133 Rs132
            2024-09-23 1:34 Rs1021.1 Rs956 Rs737
            2023-04-22 17:12 Rs1201 Rs420 Rs240
        Output:YYYY-MM-DD,HH:MM,High,Curremt,Low
                2024-09-22,15:09,Rs134,Rs133,Rs132
                2024-09-23,1:34,Rs1021.1,Rs956,Rs737
                2023-04-22,17:12,Rs1201,Rs420,Rs240
    """), ChatMessage(role="user",content=f"The below data given is a set of logs of process of a system, order them in a csv manner, Data: {read_logs}")]
        res = self.gemma_llm.chat(messages)
        return res