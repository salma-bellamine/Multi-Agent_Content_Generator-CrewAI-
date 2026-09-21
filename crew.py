import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.0
)


planner = Agent(
    role="Content Planner",

    goal=(
        "Create a detailed content plan for an article about {topic}. "
        "The target audience is {audience}. "
        "The article should contain approximately {word_count} words. "
        "The SEO keywords are: {seo_keywords}."
    ),

    backstory=(
        "You are an expert content strategist and SEO specialist. "
        "You analyze the topic, target audience, keywords and description "
        "to create a clear and useful content plan."
    ),

    llm=llm,
    allow_delegation=False,
    verbose=True
)


writer = Agent(
    role="Content Writer",

    goal=(
        "Write a high-quality article in French about {topic}. "
        "The target audience is {audience}. "
        "The article should contain approximately {word_count} words. "
        "Use the following SEO keywords naturally: {seo_keywords}. "
        "Follow the description provided by the user."
    ),

    backstory=(
        "You are a professional French content writer specialized in SEO. "
        "You write clear, engaging and well-structured articles. "
        "You use the content plan created by the planner."
    ),

    llm=llm,
    allow_delegation=False,
    verbose=True
)


editor = Agent(
    role="Content Editor",

    goal=(
        "Review and improve the French article about {topic}. "
        "Make sure that it follows the requested word count, "
        "target audience, SEO keywords and description."
    ),

    backstory=(
        "You are a professional French editor and SEO specialist. "
        "You correct grammar, spelling and style. "
        "You improve readability and remove unnecessary repetition. "
        "You ensure that the final article is ready for publication."
    ),

    llm=llm,
    allow_delegation=False,
    verbose=True
)
plan = Task(
    description=(
        "Create a detailed content plan for the following article.\n\n"
        "Topic: {topic}\n"
        "Target audience: {audience}\n"
        "Number of words: {word_count}\n"
        "SEO keywords: {seo_keywords}\n"
        "Description: {description}\n\n"

        "The plan must include:\n"
        "1. A suitable title\n"
        "2. Introduction\n"
        "3. Main sections and subsections\n"
        "4. Important points to explain\n"
        "5. SEO keyword placement\n"
        "6. Conclusion"
    ),

    expected_output=(
        "A detailed content plan in French, "
        "structured with headings and subsections."
    ),

    agent=planner
)
write = Task(
    description=(
        "Write the complete article in French based on the content plan.\n\n"
        "Topic: {topic}\n"
        "Target audience: {audience}\n"
        "Target word count: {word_count}\n"
        "SEO keywords: {seo_keywords}\n"
        "Description: {description}\n\n"

        "The article must:\n"
        "- Be written entirely in French\n"
        "- Respect the target audience\n"
        "- Respect the requested approximate word count\n"
        "- Naturally integrate the SEO keywords\n"
        "- Have a clear introduction\n"
        "- Have structured headings\n"
        "- Have a conclusion\n"
        "- Be formatted in Markdown"
    ),

    expected_output=(
        "A complete French article in Markdown format, "
        "ready for editing."
    ),

    agent=writer
)
edit = Task(
    description=(
        "Review the article produced by the writer.\n\n"
        "Check:\n"
        "- French grammar and spelling\n"
        "- Clarity and readability\n"
        "- Structure\n"
        "- SEO keyword integration\n"
        "- Target audience\n"
        "- Requested approximate word count\n"
        "- Consistency with the description\n\n"

        "Return only the final polished article in Markdown."
    ),

    expected_output=(
        "A polished and publication-ready French article "
        "in Markdown format."
    ),

    agent=editor
)
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=True
)

def generate_article(
    topic,
    audience,
    word_count,
    seo_keywords,
    description
):

    result = crew.kickoff(
        inputs={
            "topic": topic,
            "audience": audience,
            "word_count": word_count,
            "seo_keywords": seo_keywords,
            "description": description
        }
    )

    return result