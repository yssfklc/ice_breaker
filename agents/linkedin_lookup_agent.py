from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import (
    initialize_agent,
    Tool,
    AgentType,
    AgentExecutor,
    create_react_agent,
)
from agents.tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = "given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.Your answer should contain only a URL"
    prompt_template = PromptTemplate(
        template=template,  # Add the missing variables
        input_variables=["name_of_person"],
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful when you need to get the Twitter Page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    linkedin_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name))

    return linkedin_profile_url


# New Components


# agent_executer = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)  # Pass the created agent

# result = agent_executer.invoke({"input": name})  # Provide the name as input
# result = agent_executer.invoke({"name_of_person": name}, handle_parsing_errors=True)
# Return the result (presumably the LinkedIn URL)
