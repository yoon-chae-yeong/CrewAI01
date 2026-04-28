# CrewAI 시장 조사(Market Research) 예제

CrewAI로 **시장 조사**용 멀티 에이전트 크루를 구성하는 예제입니다. 에이전트 역할명은 다음 흐름을 따릅니다.

| 순서 | 에이전트 컨셉 |
|------|----------------|
| 1 | Research — 1차 시장·환경 리서치 |
| 2 | Opportunity — 기회 분석 |
| 3 | Growth — 성장 전략·시나리오 |
| 4 | Business Case — 비즈니스 케이스 통합 |
| 5 | Validation — 최종 검증·보고서 정리 |

작업은 **순차 실행**되며, 앞 단계 결과가 다음 단계 컨텍스트로 전달됩니다.

## 사전 요구 사항

- Python 3.10 이상 권장
- [uv](https://docs.astral.sh/uv/) 설치 (미설치 시): [공식 설치 방법](https://docs.astral.sh/uv/getting-started/installation/) 참고

## 가상환경 만들기 및 의존성 설치

프로젝트 루트에서:

```bash
uv venv
```

가상환경 활성화 후 **`uv pip install`**으로 패키지를 넣습니다. (`uv venv`만 쓴 환경에는 `pip` 명령이 없을 수 있어 `python -m pip` 대신 `uv pip`을 쓰는 것이 안전합니다.)

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

### Windows (cmd)

```cmd
.\.venv\Scripts\activate.bat
uv pip install -r requirements.txt
```

### macOS / Linux

```bash
source .venv/bin/activate
uv pip install -r requirements.txt
```

활성화 없이 특정 파이썬에 설치하려면:

```bash
uv pip install -r requirements.txt --python .venv/Scripts/python.exe
```

(Windows 경로 예시; macOS/Linux는 `.venv/bin/python`.)

## 환경 변수

실행하려면 LLM API 키가 필요합니다. 프로젝트 루트에 `.env` 파일을 만들고 예를 들어 다음을 설정하세요.

- `OPENAI_API_KEY` — 사용하는 LLM 제공자에 맞는 키 (예: OpenAI)

웹 검색·스크래핑 도구를 쓰려면 Serper 등 해당 서비스 키도 필요합니다.

- `SERPER_API_KEY` — `SerperDevTool` 사용 시

## 실행

가상환경이 활성화된 상태에서:

```bash
python main.py
```

실행하면 터미널에서 **시장 조사 주제**를 묻는 프롬프트가 나옵니다. 한 줄로 입력하면 그 문자열이 `{topic}`에 들어갑니다. 빈 입력은 허용되지 않으며 다시 입력을 요청합니다.

완료 후 같은 디렉터리에 **`market_research.md`**가 생성됩니다.



## 실습 과제 (확장)

현재 예제는 핵심 5단계 에이전트만 포함합니다. 실습자는 아래 3개 에이전트를 직접 추가해 보세요.

| 순서 | 에이전트 컨셉 |
|------|----------------|
| 4 | Risk — 리스크 식별 |
| 5 | Failure Analysis — 실패 사례·교훈 |
| 6 | Devil's Advocate — 가정 비판·반론 |

실습 가이드:
- `main.py`에 각 에이전트와 해당 `Task`를 정의합니다.
- `context` 체인을 연결해 앞 단계 결과가 다음 단계로 전달되게 구성합니다.
- `Crew(agents=[...], tasks=[...])` 목록에 새 에이전트/태스크를 포함합니다.
