from dotenv import load_dotenv

from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

load_dotenv(dotenv_path=".env")

topic = "Medical Industry using Generative AI"

# tool 1
llm = LLM(model="gpt-4o-mini")

# tool 2
search_tool = SerperDevTool(n=10)

# agent 1
senior_research_analyst = Agent(
    role="Senior Research Analyst",
    goal=f"Research, analyze and synthesize comprehensive information on the {topic} from reliable web sources",
    backstory=(
        "You're an expert research analyst with advanced web research skills. "
        "You excel at finding, analyzing and synthesizing information from various sources using tools. "
        "You're also skilled at distinguishing between reliable and unreliable sources, fact-checking, "
        "cross-referencing information, and identifying key patterns and insights. You provide well-organized "
        "research breifs with proper citations and source verfications. Your analysis includes both raw data "
        "and interpreted insights, making complex information accessible and actionalbe."
    ),
    allow_delegation=False,
    verbose=True,
    tools=[search_tool],
    llms=llm,
)

# agent 2
content_writer = Agent(
    role="Content Writer",
    goal="Transform reserach fidings into engaging blog posts while maintaining accuracy",
    backstory=(
        "You're a skilled content writer specilized in creating engaging, accessible content from "
        "technical reserach. You work closely with the Senior Research Analyst and excel at maintaining "
        "perfect balance between information and entertaining writing, while ensuring all facts and "
        "citations from the research are properly incorporated. You have a talent for making complex "
        "topic approachable without oversimplifying them."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm,
)

# research task
research_task = Task(
    description=(
        """
        1. Conduct comprehensive rsearch on {topic} including:
            - Recent developments and nws
            - Key industry trends and innovations
            - Experts opinions and analyses
            - Statistical data and market insights
        2. Evaluate source credibility and fact-check all information
        3. Organize findings into a structured research brief
        4. Include all relevant citations and sources
        """
    ),
    expected_output=(
        """
        A detailed research report containing:
            - Executive summary of key findings
            - Comprehensive analysis of current trends and developments
            - List of verified facts and statistics
            - All citations and links to original sources
            - Clear categorization of main themes and patterns
        Please format with clear sections and bullet points for easy reference.
        """
    ),
    agent=senior_research_analyst,
)

# content writing task
writing_task = Task(
    description=(
        """
        Using the research brief provided, create an engaging blog post that:
        1. Tranforms technical information into accessible content
        2. Maintains all factual accuracy and citations from the research
        3. Includes:
            - Attention-grabbing introduction
            - Welll-structured body sections with clear headings
            - Compelling conclusion
        4. Preserves all source citations in [Source: URL] format
        5. Includes a References section at the end
        """
    ),
    expected_output=(
        """
        A polished blog post in markdown format that:
            - Engages readers while maintaining accuracy
            - Contains properly structured sections
            - Includes Inline citations hyperlinked to the original source url
            - Presents information in an accessible yet informative way
            - Follows proper markdown formatting, use H1 for the title and H3 for subsections
        """
    ),
    agent=content_writer,
)

crew = Crew(
    agents=[senior_research_analyst, content_writer],
    tasks=[research_task, writing_task],
    verbose=True,
    memory=False,
)


def generate_content(topic: str):
    return crew.kickoff(inputs={"topic": topic})


if __name__ == "__main__":
    result = crew.kickoff(inputs={"topic": topic})
    print(result)
