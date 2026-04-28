from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv

# API 키 로드
load_dotenv()
# 또는 직접 설정
# import os
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# 웹 검색 및 스크래핑 도구 설정 (선택사항) — 시장조사 1단계에서 사용
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# --- 에이전트 (이름/역할은 market research 멀티에이전트 구성에 맞춤) ---

research_agent = Agent(
    role="리서치 에이전트 (Research)",
    goal="대상 시장·주제에 대한 정확하고 포괄적인 1차 정보 수집",
    backstory=(
        "시장 규모, 경쟁, 최신 동향, 규제, 고객 세그먼트를 빠짐없이 조사하는 시장 리서처입니다. "
        "출처와 근거를 명확히 남깁니다."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool],
)

opportunity_agent = Agent(
    role="기회 분석 에이전트 (Opportunity)",
    goal="리서치 결과에서 성장 기회와 매력적인 진입 포인트를 도출",
    backstory=(
        "트렌드와 공백 시장을 읽어 비즈니스 기회를 구조화하는 전략 컨설턴트입니다."
    ),
    verbose=True,
    allow_delegation=False,
)

growth_agent = Agent(
    role="성장 전략 에이전트 (Growth)",
    goal="기회를 바탕으로 실행 가능한 성장 가설과 확장 시나리오 제시",
    backstory=(
        "GTM, 채널, 단계별 성장 로드맵을 설계해 온 그로스 전략가입니다."
    ),
    verbose=True,
    allow_delegation=False,
)

business_case_agent = Agent(
    role="비즈니스 케이스 에이전트 (Business Case)",
    goal="앞선 분석을 통합해 투자·실행 여부를 판단할 수 있는 비즈니스 케이스 초안 작성",
    backstory=(
        "가설, 근거, 재무·전략적 함의를 한데 묶어 의사결정용 요약을 만드는 FP&A·전략 담당입니다."
    ),
    verbose=True,
    allow_delegation=False,
)

validation_agent = Agent(
    role="검증 에이전트 (Validation)",
    goal="비즈니스 케이스의 논리 일관성·근거 충분성·실행 가능성을 최종 점검하고 개선안 제시",
    backstory=(
        "체크리스트와 실무 기준으로 최종 산출물의 품질을 보증하는 검토자입니다."
    ),
    verbose=True,
    allow_delegation=False,
)

# --- 작업 정의 (순차 컨텍스트 체인) ---

research_task = Task(
    description="""'{topic}'를 중심으로 시장 조사를 수행하세요.
    시장 규모·성장률, 주요 플레이어, 고객 니즈, 규제·기술 동향 등을 조사하고
    신뢰 가능한 근거와 출처를 함께 제시하세요.""",
    agent=research_agent,
    expected_output="""구조화된 1차 시장 리서치 요약(사실·수치·출처·가정 명시).""",
)

opportunity_task = Task(
    description="""앞선 리서치를 바탕으로 '{topic}' 영역에서의 기회를 정리하세요.
    세그먼트별 매력도, 차별화 포인트, 단기·중기 기회를 구분해 서술하세요.""",
    agent=opportunity_agent,
    expected_output="""기회 목록, 근거, 우선순위 초안.""",
    context=[research_task],
)

growth_task = Task(
    description="""도출된 기회를 실행하기 위한 성장 전략 가설과 단계별 시나리오를 제시하세요.
    '{topic}'에 맞는 채널·파트너·마일스톤을 포함하세요.""",
    agent=growth_agent,
    expected_output="""성장 가설, 로드맵 초안, 주요 KPI 제안.""",
    context=[opportunity_task],
)

business_case_task = Task(
    description="""전 단계까지의 내용을 통합해 의사결정용 비즈니스 케이스 초안을 작성하세요.
    '{topic}'에 대한 권고 요지, 핵심 근거, 다음 액션을 명확히 하세요.""",
    agent=business_case_agent,
    expected_output="""비즈니스 케이스 초안(요약·근거·권고·리스크 요약).""",
    context=[growth_task],
)

validation_task = Task(
    description="""비즈니스 케이스 초안을 최종 검증하세요.
    논리 비약, 근거 부족, 실행 불가능한 부분을 지적하고 수정·보완된 최종 시장 조사 보고서 형태로 정리하세요.""",
    agent=validation_agent,
    expected_output="""최종 시장 조사 보고서(검증 코멘트·개선 반영본).""",
    context=[business_case_task],
)

# 크루 구성 및 실행
market_research_crew = Crew(
    agents=[
        research_agent,
        opportunity_agent,
        growth_agent,
        business_case_agent,
        validation_agent,
    ],
    tasks=[
        research_task,
        opportunity_task,
        growth_task,
        business_case_task,
        validation_task,
    ],
    process=Process.sequential,
    verbose=True,
)


def read_topic_from_terminal() -> str:
    """사용자가 터미널에서 시장 조사 주제를 입력한다."""
    topic = input("시장 조사 주제를 입력하세요: ").strip()
    while not topic:
        topic = input("주제가 비었습니다. 다시 입력하세요: ").strip()
    return topic


if __name__ == "__main__":
    user_topic = read_topic_from_terminal()
    result = market_research_crew.kickoff(inputs={"topic": user_topic})

    print(result)

    with open("market_research.md", "w", encoding="utf-8") as f:
        f.write(str(result))
