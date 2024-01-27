from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup
from agents.twitter_lookup_agent import twitter_lookup_agent
from output_parsers import person_intel_parser, PersonIntel
import os


def ice_break(name) -> [PersonIntel, str]:
    linkedin_profile_url = lookup(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url)
    twitter_username = twitter_lookup_agent(name=name)
    twitter_data = scrape_user_tweets(username=twitter_username, num_tweets=2)

    summary_template = """
        given the information {linkedin_information} and {twitter_information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about these
        3. A topic that may interest
        4. 2 creative ice breakers to open a conversation with them
        \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.invoke(
        {"linkedin_information": linkedin_data, "twitter_information": twitter_data}
    )

    return person_intel_parser(result)


if __name__ == "__main__":
    ice_break()
