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

risk_agent = Agent(
    role="리스크 에이전트 (Risk)",
    goal="시장·운영·재무·규제 관점의 주요 리스크를 식별하고 우선순위화",
    backstory=(
        "불확실성과 다운사이드를 체계적으로 목록화하는 리스크 분석 전문가입니다."
    ),
    verbose=True,
    allow_delegation=False,
)

failure_analysis_agent = Agent(
    role="실패 분석 에이전트 (Failure Analysis)",
    goal="유사 시장·유사 제품의 실패 사례와 원인을 분석해 교훈 도출",
    backstory=(
        "포스트모템과 산업 사례를 통해 '왜 실패했는지'를 명료하게 정리합니다."
    ),
    verbose=True,
    allow_delegation=False,
)

devils_advocate_agent = Agent(
    role="악마의 변호인 에이전트 (Devil's Advocate)",
    goal="합의된 가정을 의도적으로 비판해 논리 구멍과 과대평가 지점 노출",
    backstory=(
        "낙관적 결론에 균형을 주기 위해 반론과 대안 시나리오를 날카롭게 제시합니다."
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

risk_task = Task(
    description="""'{topic}' 진입·성장 시 예상되는 리스크를 분류하고(시장·운영·규제·재무 등)
    영향도와 발생 가능성 관점에서 정리하세요.""",
    agent=risk_agent,
    expected_output="""리스크 매트릭스 또는 목록, 완화 방향 초안.""",
    context=[growth_task],
)

failure_analysis_task = Task(
    description="""유사 산업·유사 모델의 실패 사례를 참고해 '{topic}' 관련 함정과 반복되는 실패 원인을 분석하세요.""",
    agent=failure_analysis_agent,
    expected_output="""실패 패턴, 교훈, 회피·완화 아이디어.""",
    context=[risk_task],
)

devils_advocate_task = Task(
    description="""지금까지의 낙관적 전제와 결론을 비판적으로 검토하세요.
    '{topic}' 사업/전략이 실패할 수 있는 논리적 경로를 반드시 포함하세요.""",
    agent=devils_advocate_agent,
    expected_output="""반론 요지, 재검토해야 할 가정, 대안 시나리오.""",
    context=[failure_analysis_task],
)

business_case_task = Task(
    description="""전 단계까지의 내용을 통합해 의사결정용 비즈니스 케이스 초안을 작성하세요.
    '{topic}'에 대한 권고 요지, 핵심 근거, 다음 액션을 명확히 하세요.""",
    agent=business_case_agent,
    expected_output="""비즈니스 케이스 초안(요약·근거·권고·리스크 요약).""",
    context=[devils_advocate_task],
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
        risk_agent,
        failure_analysis_agent,
        devils_advocate_agent,
        business_case_agent,
        validation_agent,
    ],
    tasks=[
        research_task,
        opportunity_task,
        growth_task,
        risk_task,
        failure_analysis_task,
        devils_advocate_task,
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
