from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools.reasoning import ReasoningTools

def create_agent():
    """Cria e configura um agente."""

    memory = Memory(
        model=OpenAIChat(id="gpt-5-nano"),
        db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
        delete_memories=True,
        clear_memories=True
    )

    agent = Agent(
        model=OpenAIChat(id="gpt-5-nano"),
        tools=[
            ReasoningTools(add_instructions=True),
        ],
        #user_id="Gabriel",
        instructions="Seja direto nas suas respostas.",
        description="Você é um assistente inteligente prestativo.",
        markdown=True,
        memory=memory,
        enable_agentic_memory=True,
    )
    
    return agent