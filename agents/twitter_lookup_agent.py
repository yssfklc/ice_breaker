from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import (
    initialize_agent,
    Tool,
    AgentType,
)
from agents.tools.tools import get_profile_url


def twitter_lookup_agent(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = "given the name {name_of_person} I want you to get it me a link to their Twitter profile page.Your answer should contain a username"
    prompt_template = PromptTemplate(
        template=template,  # Add the missing variables
        input_variables=["name_of_person"],
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 twitter profile page",
            func=get_profile_url,
            description="useful when you need to get the linkedin Page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    twitter_username = agent.run(prompt_template.format_prompt(name_of_person=name))

    return twitter_username
