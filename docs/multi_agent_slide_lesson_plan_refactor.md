# Kế hoạch refactor: Làm rõ pipeline multi-agent cho Slide/Lesson Plan

## Hiện trạng

Luồng tạo slide và giáo án hiện được triển khai bằng LangGraph supervisor trong `src/llm/graphs/content_supervisor.py`. Supervisor gọi `generate_outline`, `generate_content`, `generate_media`, `generate_quiz`, `merge_results`, và `check_quality` thông qua `ToolNode`, còn logic chuyên biệt thật sự nằm trong `src/llm/handlers/content/slide_agents/`.

Luồng hiện tại chạy được, nhưng về mặt kiến trúc nó giống orchestration qua tool hơn là một multi-agent system rõ nghĩa. Các "agent" chủ yếu là wrapper gọi LLM và trả `AgentResult`; chúng chưa nhận task envelope rõ ràng, chưa báo cáo tool usage, chưa có metadata thực thi ở cấp agent, và chưa trao đổi qua một contract agent-to-agent cụ thể.

## Trạng thái triển khai hiện tại

Refactor A2A-lite nội bộ đã được triển khai cho luồng slide/lesson-plan ở mức in-process:

- Đã thêm `AgentTask` và `AgentTaskResult` trong `src/schemas/agent_protocol.py`.
- Đã thêm package `src/llm/agents/` với các adapter: `PedagogyPlannerAgent`, `ContentDraftingAgent`, `ContentAssessmentAgent`, `MediaResearchAgent`, và `QualityReviewerAgent`.
- Các tool trong `src/llm/graphs/tools.py` hiện đóng vai trò agent dispatch adapters: build `AgentTask`, gọi specialist agent, rồi trả `AgentTaskResult` dạng JSON.
- `post_tool_processor()` trong `src/llm/graphs/content_supervisor.py` đã parse được cả format mới `AgentTaskResult` và format legacy payload-only.
- `ContentSupervisorState` đã có `agent_tasks`, `agent_results`, và `artifacts`.
- `SlideService` đã lưu compact `agent_results` summary vào `slide_state.slide_output`, không lưu full prompt/context.
- `merge_results` vẫn là deterministic service/tool, không bị đổi thành agent.

Phần chưa triển khai trong lần này:

- Chưa thêm MCP-backed media search thật.
- Chưa thêm pytest chính thức; mới có compile check và test script nhỏ cho `post_tool_processor`.
- Chưa rename/move các class cũ trong `src/llm/handlers/content/slide_agents/`; hiện chúng vẫn là implementation workers phía sau adapter mới.
- Quiz standalone vẫn nằm ở `QuizService`, không đưa vào multi-agent pipeline trong phase này để giữ ổn định phần tracker/interact/scoring.

## Trạng thái mục tiêu

Pipeline slide và lesson plan nên thể hiện rõ phân tầng:

- `ContentSupervisor`: lập kế hoạch và điều phối các specialist agent.
- Specialist agents: nhận task envelope, dùng local/internal tools khi cần, và trả structured task result.
- Tools/MCP tools: cung cấp các năng lực hẹp như media search, artifact lookup, citation verification, render/export, hoặc truy cập retrieval.
- Deterministic services: giữ các thao tác thuần xác định như merge, không gọi chúng là agent.

Phiên bản refactor đầu tiên nên dùng protocol A2A-lite nội bộ, chưa cần full distributed A2A. MCP chỉ nên thêm ở nơi có giá trị thật, đặc biệt là media research và sau này có thể là artifact/render/export.

Pipeline này cover cả `slide` và `lesson_plan` bằng cùng một `ContentSupervisor`. Khác biệt nghiệp vụ được truyền qua `task_type` và prompt/template tương ứng; không tách thành hai supervisor riêng để tránh duplicate orchestration logic.

## Quyết định kiến trúc

Không MCP-wrap mọi task nhỏ của agent.

`OutlineAgent`, `ContentAgent`, và `QuizAgent` có thể tiếp tục là in-process specialist agents. Task hiện tại của chúng chưa đủ lớn để đáng tách thành MCP tools bên ngoài. `MediaAgent` là ứng viên mạnh nhất cho MCP-backed tools vì nó tự nhiên cần năng lực ngoài như image search, URL validation, source filtering, và attribution.

Refactor nên làm cho agent rõ ràng hơn trước, rồi mới tính chuyện phân tán chúng.

## Ranh giới agent mục tiêu

| Agent | Trách nhiệm | Nhu cầu tool |
| --- | --- | --- |
| `PedagogyPlannerAgent` | Xây mục tiêu học tập, outline, trình tự bài học, kế hoạch slide/section | Thấp |
| `ContentDraftingAgent` | Viết nội dung chi tiết cho slide hoặc section giáo án từ outline và source chunks | Trung bình, chủ yếu là chunk lookup/citation check nội bộ |
| `ContentAssessmentAgent` | Sinh đánh giá/câu hỏi nhúng trong artifact slide hoặc giáo án | Trung bình |
| `MediaResearchAgent` | Tìm/gợi ý visual và gắn metadata media có thể dùng được | Cao, nên MCP-backed về sau |
| `QualityReviewerAgent` | Review factuality, coverage, pedagogy, và output format | Trung bình |
| `SlideMerger` | Merge deterministic các artifact thành slide cuối | Nên giữ là service/tool, không phải agent |

`ContentAssessmentAgent` không thay thế luồng quiz standalone. Nó chỉ sinh assessment nhúng trong content artifact. Quiz standalone tiếp tục dùng `QuizService` để maintain được `QuizRound`, `QuestionRecord`, `StudentTracker`, chấm điểm, review câu sai, và thống kê.

## File bị ảnh hưởng

| File | Loại thay đổi | Phụ thuộc |
| --- | --- | --- |
| `src/schemas/agent_protocol.py` | tạo mới | Chặn toàn bộ agent adapter và graph changes |
| `src/llm/agents/__init__.py` | tạo mới | Phụ thuộc protocol |
| `src/llm/agents/base.py` | tạo mới | Phụ thuộc protocol |
| `src/llm/agents/slide_planner.py` | tạo mới | Wrap `OutlineAgent` hiện tại |
| `src/llm/agents/content_drafting.py` | tạo mới | Wrap `ContentAgent` hiện tại |
| `src/llm/agents/content_assessment.py` | tạo mới | Wrap `QuizAgent` hiện tại cho assessment nhúng |
| `src/llm/agents/slide_content.py` | compatibility alias | Alias tới `ContentDraftingAgent` |
| `src/llm/agents/assessment.py` | compatibility alias | Alias tới `ContentAssessmentAgent` |
| `src/llm/agents/media_research.py` | tạo mới | Wrap `MediaAgent` hiện tại, sau đó nối MCP |
| `src/llm/agents/quality.py` | tạo mới | Wrap `BaseQualityReviewer` hiện tại |
| `src/llm/handlers/content/slide_agents/base_slide_agent.py` | chỉnh sửa | Thêm compatibility path hoặc migrate sau base mới |
| `src/llm/graphs/state.py` | chỉnh sửa | Thêm task/artifact fields và agent execution log |
| `src/llm/graphs/tools.py` | chỉnh sửa | Thay direct tool wrappers bằng agent dispatch adapters |
| `src/llm/graphs/content_supervisor.py` | chỉnh sửa | Supervisor route agent tasks và consume task results |
| `src/schemas/slide_schemas.py` | chỉnh sửa | Giữ payload models, có thể thêm artifact aliases |
| `src/llm/services/slide_service.py` | chỉnh sửa | Xử lý graph result giàu metadata hơn và lưu agent execution metadata |
| `src/llm/services/slide_merger.py` | chỉnh sửa | Nhận artifacts từ protocol result mà không coi merge là agent |
| `src/tools/mcp_client.py` | chỉnh sửa sau | Chỉ dùng khi thêm MCP-backed media/search/export |
| `src/tools/implementations/web_search_tool.py` | chỉnh sửa sau | Ứng viên hỗ trợ media/search |
| `docs/multi_agent_slide_lesson_plan_refactor.md` | tạo mới | Tài liệu kế hoạch |

## Protocol đề xuất

Tạo `src/schemas/agent_protocol.py` với các contract sau:

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal

AgentStatus = Literal["success", "partial", "failed", "blocked"]

@dataclass
class AgentTask:
    task_id: str
    from_agent: str
    to_agent: str
    task_type: str
    objective: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    context_refs: List[str] = field(default_factory=list)
    expected_artifact: Optional[str] = None
    revision_instruction: Optional[str] = None

@dataclass
class AgentTaskResult:
    task_id: str
    agent_id: str
    status: AgentStatus
    task: Optional[Dict[str, Any]] = None
    artifact_type: Optional[str] = None
    artifact: Dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    used_tools: List[str] = field(default_factory=list)
    latency_ms: int = 0
    error_code: Optional[str] = None
    error_message: Optional[str] = None
```

Protocol này cố ý nhỏ gọn. Nó đủ để thể hiện giao tiếp agent-to-agent mà chưa ép hệ thống phải có distributed runtime.

## Kế hoạch triển khai

### Phase 1: Types và Interfaces

- [ ] Step 1.1: Thêm `src/schemas/agent_protocol.py`.
  - Định nghĩa `AgentTask`, `AgentTaskResult`, `AgentMessage` nếu cần, và status literals.
  - Chỉ thêm `to_dict()` / `from_dict()` nếu serialize dataclass trực tiếp gây rườm rà.
  - Verify: `python3 -m py_compile src/schemas/agent_protocol.py`.

- [ ] Step 1.2: Thêm `src/llm/agents/base.py`.
  - Định nghĩa `BaseAgent` với `agent_id`, `run_task(task: AgentTask) -> AgentTaskResult`, và protected method `_run(task)`.
  - Giữ base này độc lập với LangGraph.
  - Verify: `python3 -m py_compile src/llm/agents/base.py`.

- [ ] Step 1.3: Thêm execution log của agent vào `ContentSupervisorState` trong `src/llm/graphs/state.py`.
  - Thêm `agent_tasks: list`, `agent_results: list`, và `artifacts: dict`.
  - Giữ các field hiện có như `outline_payload`, `content_payload`, `media_payload`, `quiz_payload`, và `merged_slides` để backward compatibility.
  - Verify: `python3 -m py_compile src/llm/graphs/state.py`.

### Phase 2: Agent Adapters

- [ ] Step 2.1: Tạo `src/llm/agents/slide_planner.py`.
  - Wrap `OutlineAgent` hiện tại.
  - Convert `AgentTask.inputs` thành kwargs cho `OutlineAgent.run(...)`.
  - Trả `AgentTaskResult(artifact_type="outline_payload")`.
  - Verify: một script nhỏ có thể instantiate agent bằng mock task và nhận `outline_payload` hoặc structured failure.

- [ ] Step 2.2: Tạo `src/llm/agents/slide_content.py`.
  - Wrap `ContentAgent` hiện tại.
  - Nhận `outline_payload`, `chunk_map`, `task_type`, và optional `revision_instruction`.
  - Trả `artifact_type="content_payload"`.
  - Verify: mock task với một outline slide và một chunk trả về `slides`.

- [ ] Step 2.3: Tạo `src/llm/agents/assessment.py`.
  - Wrap `QuizAgent` hiện tại.
  - Nhận `topic`, `context_map`, và constraints như `max_questions`.
  - Trả `artifact_type="quiz_payload"`.
  - Verify: mock task trả về `quiz_items` hoặc structured failure.

- [ ] Step 2.4: Tạo `src/llm/agents/media_research.py`.
  - Wrap `MediaAgent` hiện tại trước.
  - Tạm đặt `used_tools=[]`.
  - Chừa extension point rõ ràng cho MCP-backed `image_search` và `url_validator`.
  - Verify: mock task trả về `hero_media` và `inline_media`.

- [ ] Step 2.5: Tạo `src/llm/agents/quality.py`.
  - Wrap `get_quality_reviewer(task_type)`.
  - Trả `artifact_type="quality_review"`.
  - Verify: mock task trả về dict tương thích `QualityReviewResult`.

### Phase 3: Tích hợp vào Graph

- [ ] Step 3.1: Thay direct specialist calls trong `src/llm/graphs/tools.py` bằng agent dispatch wrappers.
  - Tạm giữ nguyên tên tool: `generate_outline`, `generate_content`, `generate_media`, `generate_quiz`, `check_quality`.
  - Bên trong mỗi tool, build `AgentTask`, gọi agent adapter tương ứng, và return serialized `AgentTaskResult`.
  - `merge_results` vẫn nên là deterministic tool/service.
  - Verify: `python3 -m py_compile src/llm/graphs/tools.py`.

- [ ] Step 3.2: Cập nhật `post_tool_processor()` trong `src/llm/graphs/content_supervisor.py`.
  - Parse `AgentTaskResult`.
  - Lưu raw task result vào `agent_results`.
  - Lưu `artifact` vào cả `artifacts[artifact_type]` và legacy state key từ `TOOL_STATE_MAPPING`.
  - Tiếp tục support old payload-only response trong giai đoạn chuyển tiếp.
  - Verify: chạy unit-style script feed fake `ToolMessage` và kiểm tra state updates.

- [ ] Step 3.3: Cập nhật supervisor prompt trong `src/llm/graphs/content_supervisor.py`.
  - Mô tả specialist agents là agents, không chỉ là tools.
  - Nói rõ supervisor delegate task và nhận artifacts.
  - Giữ thứ tự bắt buộc hiện tại: planner, content, optional media/assessment, merge, quality.
  - Verify: inspect prompt text được sinh ra cho cả `slide` và `lesson_plan`.

- [ ] Step 3.4: Cập nhật reflection logic.
  - Reflection nên tạo revision task cho đúng agent chịu trách nhiệm artifact bị lỗi.
  - `revise_outline` clear outline/content/merged artifacts.
  - `revise_content` clear content/merged artifacts.
  - `revise_quiz` clear quiz/merged artifacts nếu có quiz.
  - Verify: simulated quality review results route tới đúng graph node tiếp theo.

### Phase 4: Điều chỉnh Service và Persistence

- [ ] Step 4.1: Cập nhật `src/llm/services/slide_service.py`.
  - Lưu summary của `agent_results` vào `slide_state.slide_output`.
  - Không lưu full prompt text hoặc full context map vào session JSON.
  - Giữ nguyên response format đang hiển thị cho user.
  - Verify: generate flow với `auto_approve_outline=True` vẫn lưu `slides`, `quality_review`, và `_task_type`.

- [ ] Step 4.2: Cập nhật `src/llm/services/slide_merger.py`.
  - Nhận được cả legacy `AgentResult` payloads hoặc `AgentTaskResult.artifact`.
  - Giữ merge là deterministic.
  - Verify: direct merge test với outline/content/media/quiz artifacts trả `MergedSlide` list.

- [ ] Step 4.3: Chỉ cập nhật `src/schemas/slide_schemas.py` nếu thật sự cần.
  - Giữ các payload model hiện tại như artifact schema.
  - Tránh duplicate `AgentResult` và `AgentTaskResult`; coi `AgentResult` là legacy/internal LLM-call envelope.
  - Verify: `python3 -m py_compile src/schemas/slide_schemas.py`.

### Phase 5: MCP Integration, chỉ ở nơi hữu ích

- [ ] Step 5.1: Định nghĩa media tool interface cho `MediaResearchAgent`.
  - Candidate tools: `image_search`, `url_validator`, `source_attribution`.
  - Bắt đầu bằng local adapters có thể chuyển sang MCP sau.
  - Verify: media agent báo `used_tools=["image_search"]` khi tool path được bật.

- [ ] Step 5.2: Chỉ thêm MCP-backed media search sau khi agent protocol đã ổn định.
  - Tích hợp qua `src/tools/mcp_client.py` hoặc một media tool implementation riêng.
  - Giữ fallback behavior: nếu MCP fail, trả media suggestions không có URL thay vì làm fail toàn bộ slide pipeline.
  - Verify: tắt MCP credentials/network và xác nhận slide generation vẫn hoàn thành.

- [ ] Step 5.3: Cân nhắc MCP tools cho artifact rendering/export về sau.
  - Candidate tools: `render_html`, `export_pptx`, `export_pdf`.
  - Không đưa vào refactor đầu tiên nếu export slide chưa phải requirement ngay.

### Phase 6: Tests và Verification

- [ ] Step 6.1: Thêm tests cho protocol serialization và adapter behavior.
  - Suggested path: `tests/llm/test_agent_protocol.py`.
  - Verify: `python3 -m pytest tests/llm/test_agent_protocol.py`.

- [ ] Step 6.2: Thêm tests cho `post_tool_processor`.
  - Suggested path: `tests/llm/graphs/test_content_supervisor_agent_results.py`.
  - Cover cả response mới dạng `AgentTaskResult` và response cũ dạng payload-only.
  - Verify: `python3 -m pytest tests/llm/graphs/test_content_supervisor_agent_results.py`.

- [ ] Step 6.3: Thêm smoke test cho slide pipeline với mocked agents.
  - Suggested path: `tests/llm/services/test_slide_pipeline_agents.py`.
  - Mock LLM calls để tránh phụ thuộc external API.
  - Verify: `python3 -m pytest tests/llm/services/test_slide_pipeline_agents.py`.

- [ ] Step 6.4: Chạy baseline compile check.
  - Verify: `python3 -m compileall src/llm src/schemas`.

### Phase 7: Cleanup và Documentation

- [ ] Step 7.1: Chỉ rename old `slide_agents` sau khi adapters đã ổn định.
  - Option A: giữ class cũ làm implementation workers phía sau `src/llm/agents`.
  - Option B: chuyển chúng vào `src/llm/agents/legacy_workers`.
  - Ưu tiên Option A nếu code chưa quá rối.

- [ ] Step 7.2: Cập nhật `README.md` hoặc tạo `docs/architecture_multi_agent.md`.
  - Giải thích supervisor, specialist agents, tools, MCP, và deterministic services.
  - Thêm sequence diagram hoặc workflow dạng bullet.

- [ ] Step 7.3: Xóa các comment cũ mô tả sub-agent chỉ như tools.
  - Giữ public function names ổn định nếu UI/API đang phụ thuộc chúng.

## Kế hoạch rollback

### Nếu Phase 1 fail

1. Xóa `src/schemas/agent_protocol.py`, `src/llm/agents/base.py`, và `src/llm/agents/__init__.py`.
2. Revert thay đổi trong `src/llm/graphs/state.py`.
3. Verify: `python3 -m compileall src/llm src/schemas`.

### Nếu Phase 2 fail

1. Giữ protocol files nếu chúng compile được.
2. Chỉ xóa adapter file bị lỗi trong `src/llm/agents/`.
3. Graph hiện tại vẫn dùng `src/llm/handlers/content/slide_agents/*`, nên runtime behavior không đổi.
4. Verify: chạy flow slide/lesson-plan hiện tại mà không cần graph changes.

### Nếu Phase 3 fail

1. Revert `src/llm/graphs/tools.py` và `src/llm/graphs/content_supervisor.py` về direct legacy tool behavior.
2. Giữ adapter files nếu chúng không được dùng và vẫn compile.
3. Verify: chạy `python3 -m compileall src/llm src/schemas` và một manual slide generation smoke test.

### Nếu Phase 4 fail

1. Revert `src/llm/services/slide_service.py` và `src/llm/services/slide_merger.py`.
2. Chỉ giữ graph-level changes nếu graph output vẫn backward-compatible với old service processing.
3. Verify: session JSON vẫn lưu `slide_output.status`, `slides`, `total_slides`, và `quality_review`.

### Nếu Phase 5 fail

1. Disable MCP-backed media tools bằng config flag.
2. Fallback về behavior hiện tại của `MediaAgent`, nơi URL là optional.
3. Verify: slide generation hoàn thành với media payload rỗng hoặc không có URL.

## Rủi ro

1. **Protocol bị trùng vai trò với `AgentResult` hiện tại**
   - Code hiện đã có `AgentResult` trong `src/schemas/slide_schemas.py`.
   - Mitigation: coi `AgentResult` là legacy low-level LLM-call envelope, còn `AgentTaskResult` là envelope giao tiếp inter-agent.

2. **LangGraph `ToolNode` kỳ vọng output dạng string**
   - Tools hiện return JSON string và được `post_tool_processor` parse.
   - Mitigation: tiếp tục return JSON string, nhưng encode `AgentTaskResult` thay vì raw payload. Support cả hai format trong giai đoạn migration.

3. **HITL interrupt behavior có thể bị vỡ**
   - `generate_outline` hiện pause bằng `interrupt(...)`.
   - Mitigation: giữ HITL bên trong outline tool wrapper ở Phase 3. Chưa chuyển HITL vào agent adapter cho tới khi pipeline ổn định.

4. **Session JSON có thể phình lớn**
   - Agent results có thể chứa context, warnings, và artifacts.
   - Mitigation: chỉ lưu compact execution summaries trong `slide_state.slide_output`, không lưu full prompts hoặc full context maps.

5. **MCP có thể thêm complexity mà không tạo giá trị**
   - Phần lớn sub-agent task hiện tại là prompt transformation.
   - Mitigation: chỉ đưa MCP vào media search trước. Mọi MCP-backed capability phải có fallback path.

6. **Quality reflection routing có thể mơ hồ**
   - Reviewer actions cần map tới artifact và agent cụ thể.
   - Mitigation: định nghĩa mapping cố định: `revise_outline -> PedagogyPlannerAgent`, `revise_content -> ContentDraftingAgent`, `revise_quiz -> ContentAssessmentAgent`.

7. **Tests có thể gọi external LLM APIs**
   - Agents hiện gọi Gemini trực tiếp.
   - Mitigation: adapter tests nên mock old agents hoặc inject fake agents. Integration tests dùng LLM thật nên optional và được mark riêng.

8. **Trộn quiz standalone vào content pipeline làm khó maintain tracker/interact**
   - Quiz standalone có lifecycle riêng: lưu round, chấm điểm, update tracker, review câu sai, thống kê.
   - Mitigation: phase này chỉ đưa assessment nhúng của slide/lesson_plan vào content pipeline. `QuizService` vẫn sở hữu quiz standalone và state học tập.

## Tiêu chí thành công

- Workflow slide/lesson-plan có thể được giải thích như supervisor-to-agent delegation, không chỉ là tool calls.
- Mỗi specialist agent nhận `AgentTask` và trả `AgentTaskResult`.
- Graph state ghi nhận `agent_results` và `artifacts`.
- User-facing behavior của slide và lesson-plan vẫn tương thích.
- Quiz standalone, answer checking, review wrong, và student tracker không bị kéo vào content agent pipeline.
- MCP chỉ dùng ở nơi có capability thật sự hữu ích, bắt đầu từ media research.
- `merge_results` vẫn deterministic và không bị gắn nhãn nhầm là agent.

## Thứ tự triển khai đề xuất

1. Thêm protocol và base agent.
2. Thêm wrappers quanh các slide agents hiện tại.
3. Cho graph wrappers return `AgentTaskResult` trong khi giữ nguyên tool names.
4. Cập nhật post-tool processing để lưu artifacts và agent logs.
5. Cập nhật service persistence để lưu compact agent metadata.
6. Chỉ thêm MCP-backed media tools sau khi internal agent protocol chạy ổn.

## Kết quả triển khai

Các phase đã hoàn thành trong lần refactor này:

1. Phase 1: Types và Interfaces.
2. Phase 2: Agent Adapters.
3. Phase 3: Tích hợp graph với `AgentTaskResult`.
4. Phase 4: Lưu compact agent metadata trong `SlideService`.
5. Naming cleanup: dùng `ContentDraftingAgent` và `ContentAssessmentAgent` cho pipeline chung slide/lesson_plan; giữ `SlideContentAgent` và `AssessmentAgent` như compatibility alias.

Boundary sau khi triển khai:

- `ContentSupervisor` cover cả `slide` và `lesson_plan`.
- `ContentAssessmentAgent` chỉ sinh assessment nhúng trong content artifact.
- Quiz standalone vẫn đi qua `QuizService` để giữ ổn định tracker/interact/scoring.

Verification đã chạy:

```bash
python3 -m compileall src/schemas/agent_protocol.py src/llm/agents src/llm/graphs src/schemas/slide_schemas.py src/llm/services/slide_service.py
```

```bash
venv/bin/python - <<'PY'
import json
from langchain_core.messages import ToolMessage
from src.llm.graphs.content_supervisor import post_tool_processor

# Kiểm tra parser AgentTaskResult success và không resurrect artifact cũ khi result mới failed.
PY
```

Kết quả: compile pass, `post_tool_processor` test pass trong `venv`.

Việc còn lại nên làm ở task tiếp theo:

1. Thêm pytest chính thức cho protocol/adapters/post processor.
2. Chạy smoke test end-to-end với LLM thật hoặc mocked agents cho slide/lesson-plan.
3. Thiết kế MCP-backed media search sau khi internal A2A-lite đã ổn định.
