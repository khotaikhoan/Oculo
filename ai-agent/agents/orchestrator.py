"""
Multi-agent pipeline orchestrator.
Splits complex tasks into: Research → Execute → Review
Each sub-agent runs with focused context and tools.
"""
import json
import os
import anthropic
from typing import Generator
from dotenv import load_dotenv

load_dotenv()

# Đọc từ env để nhất quán với server.py
MODEL = os.getenv("MODEL", "claude-sonnet-4-5")

# ── Sub-agent system prompts ──
RESEARCH_PROMPT = """You are a Research Agent. Your job is to:
1. Analyze the task and break it into clear steps
2. Gather information needed (web search via curl, read files, check system state)
3. Return a structured research report with: findings, recommended approach, potential issues

Be thorough but concise. Output JSON with keys: findings, approach, steps, risks."""

EXECUTOR_PROMPT = """You are an Executor Agent. Your job is to:
1. Receive a research report and execute the plan step by step
2. Use tools to actually perform the work
3. Report what was done and the results

Execute precisely. Do not skip steps. Report each action taken."""

REVIEWER_PROMPT = """You are a Reviewer Agent. Your job is to:
1. Review what the Executor did
2. Verify the results are correct and complete
3. Identify any issues or improvements
4. Give a final verdict: SUCCESS, PARTIAL, or FAILED with explanation

Be critical but fair. Check actual outputs, not just intentions."""

TOOLS = [
    {"name":"run_shell","description":"Run shell command","input_schema":{"type":"object","properties":{"cmd":{"type":"string"}},"required":["cmd"]}},
    {"name":"read_file","description":"Read file content","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"write_file","description":"Write file","input_schema":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}},
    {"name":"run_applescript","description":"Run AppleScript","input_schema":{"type":"object","properties":{"script":{"type":"string"}},"required":["script"]}},
]


MAX_TOOL_ROUNDS = 20


def _run_agent(client: anthropic.Anthropic, system: str, message: str,
               use_tools: bool = True) -> tuple[str, list]:
    """Run a single agent turn, return (text_output, tool_calls_log)."""
    messages = [{"role": "user", "content": message}]
    tool_log = []
    rounds = 0

    while rounds < MAX_TOOL_ROUNDS:
        rounds += 1
        kwargs = dict(model=MODEL, max_tokens=2048, system=system, messages=messages)
        if use_tools:
            kwargs["tools"] = TOOLS

        try:
            response = client.messages.create(**kwargs)
        except Exception as e:
            return f"Error calling API: {e}", tool_log
        text_out = ""
        for block in response.content:
            if block.type == "text":
                text_out += block.text

        if response.stop_reason != "tool_use" or not use_tools:
            return text_out, tool_log

        # Execute tools
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = _execute_tool(block.name, block.input)
                tool_log.append({"tool": block.name, "input": block.input, "result": result[:300]})
                tool_results.append({"type":"tool_result","tool_use_id":block.id,"content":result})

        # Serialize content blocks
        serialized = []
        for b in response.content:
            if b.type == "text":
                serialized.append({"type":"text","text":b.text})
            elif b.type == "tool_use":
                serialized.append({"type":"tool_use","id":b.id,"name":b.name,"input":b.input})

        messages.append({"role":"assistant","content":serialized})
        messages.append({"role":"user","content":tool_results})

    return text_out, tool_log


def _execute_tool(name: str, inputs: dict) -> str:
    """Execute a tool call."""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from tools import desktop
    try:
        if name == "run_shell":    return desktop.run_shell(inputs["cmd"])
        if name == "read_file":
            p = os.path.expanduser(inputs["path"])
            with open(p, "r", errors="replace") as f: return f.read()[:4000]
        if name == "write_file":
            p = os.path.expanduser(inputs["path"])
            os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
            with open(p, "w") as f: f.write(inputs["content"])
            return f"Written: {p}"
        if name == "run_applescript": return desktop.run_applescript(inputs["script"])
        return f"Unknown tool: {name}"
    except Exception as e:
        return f"Error: {e}"


def run_pipeline(task: str, client: anthropic.Anthropic) -> Generator[dict, None, None]:
    """
    Run the full multi-agent pipeline and yield progress events.
    Yields dicts: {stage, status, content, tool_log}
    """
    # ── Stage 1: Research ──
    yield {"stage": "research", "status": "running", "content": "Analyzing task and gathering information..."}
    research_output, research_tools = _run_agent(
        client, RESEARCH_PROMPT,
        f"Task to research: {task}"
    )
    yield {"stage": "research", "status": "done", "content": research_output, "tool_log": research_tools}

    # ── Stage 2: Execute ──
    yield {"stage": "executor", "status": "running", "content": "Executing the plan..."}
    exec_message = f"""Original task: {task}

Research findings:
{research_output}

Now execute this plan step by step."""

    exec_output, exec_tools = _run_agent(client, EXECUTOR_PROMPT, exec_message)
    yield {"stage": "executor", "status": "done", "content": exec_output, "tool_log": exec_tools}

    # ── Stage 3: Review ──
    yield {"stage": "reviewer", "status": "running", "content": "Reviewing results..."}
    review_message = f"""Original task: {task}

What was executed:
{exec_output}

Tool calls made: {json.dumps(exec_tools, indent=2)}

Review the results and give your verdict."""

    review_output, _ = _run_agent(client, REVIEWER_PROMPT, review_message, use_tools=False)
    yield {"stage": "reviewer", "status": "done", "content": review_output, "tool_log": []}

    yield {"stage": "complete", "status": "done", "content": review_output}
