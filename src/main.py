from dotenv import load_dotenv
from crewai import Crew
from tasks import MeetingPrepTasks
from agents import MeetingPrepAgents


def main():
    load_dotenv()

    print("## Welcome to the Meeting Prep Crew")
    print("-------------------------------")
    meeting_participants = input(
        "What are the emails for the participants (other than you) in the meeting?\n"
    )
    meeting_context = input("What is the context of the meeting?\n")
    meeting_objective = input("What is your objective for this meeting?\n")

    tasks = MeetingPrepTasks()
    agents = MeetingPrepAgents()

    # Create agents
    research_agent = agents.research_agent()
    industry_agent = agents.industry_analysis_agent()
    strategy_agent = agents.meeting_strategy_agent()
    summary_agent = agents.summary_and_briefing_agent()

    # Create tasks
    research_task = tasks.research_task(
        research_agent, meeting_participants, meeting_context
    )
    industry_task = tasks.industry_analysis_task(
        industry_agent, meeting_participants, meeting_context
    )
    strategy_task = tasks.meeting_strategy_task(
        strategy_agent, meeting_context, meeting_objective
    )
    summary_task = tasks.summary_and_briefing_task(
        summary_agent, meeting_context, meeting_objective
    )

    strategy_task.context = [research_task, industry_task]
    summary_task.context = [research_task, industry_task, strategy_task]

    crew = Crew(
        agents=[
            research_agent,
            industry_agent,
            strategy_agent,
            summary_agent,
        ],
        tasks=[
            research_task,
            industry_task,
            strategy_task,
            summary_task,
        ],
    )

    result = crew.kickoff()

    print(result)


if __name__ == "__main__":
    main()

# help@ajd.co.kr
