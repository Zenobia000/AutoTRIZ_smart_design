"""TRIZ Rule Engine — deterministic lookup over 5 knowledge base files.

Parses KB markdown once at import, exposes pure-function lookups.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class TrizParam:
    id: int
    name_zh: str
    name_en: str
    description: str
    engineering_hints: str


@dataclass
class TrizPrinciple:
    id: int
    name_zh: str
    name_en: str
    sub_principles: list[str] = field(default_factory=list)
    engineering_hint: str = ""


@dataclass
class SeparationStrategy:
    strategy: str
    description: str
    example: str


@dataclass
class SeparationPrinciple:
    id: int
    name_zh: str
    name_en: str
    core_question: str
    strategies: list[SeparationStrategy] = field(default_factory=list)
    applicability_hint: str = ""


@dataclass
class StandardSolution:
    code: str        # "1.1.1"
    name_zh: str
    description: str
    example: str


# Su-Field state -> applicable standard solution class prefixes
SUFIELD_STATE_CLASSES: dict[str, list[str]] = {
    "incomplete":   ["1.1"],
    "harmful":      ["1.2"],
    "insufficient": ["1.3", "2.1", "2.2", "2.3", "2.4"],
    "measurement":  ["4.1", "4.2", "4.3", "4.4", "4.5"],
    "transition":   ["3.1", "3.2"],
    "simplify":     ["5.1", "5.2", "5.3", "5.4", "5.5"],
}


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def _parse_39_parameters(text: str) -> dict[int, TrizParam]:
    """Parse 01_39_parameters.md table rows."""
    params: dict[int, TrizParam] = {}
    for m in re.finditer(
        r"\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
        text,
    ):
        pid = int(m.group(1))
        if pid < 1 or pid > 39:
            continue
        params[pid] = TrizParam(
            id=pid,
            name_zh=m.group(2).strip(),
            name_en=m.group(3).strip(),
            description=m.group(4).strip(),
            engineering_hints=m.group(5).strip(),
        )
    return params


def _parse_mapping_hints(text: str) -> str:
    """Extract the LLM mapping hints YAML block."""
    m = re.search(r"映射提示:\n((?:\s+.+\n)+)", text)
    return m.group(0).strip() if m else ""


def _parse_contradiction_matrix(text: str) -> dict[tuple[int, int], list[int]]:
    """Parse 02_contradiction_matrix.md into sparse matrix."""
    matrix: dict[tuple[int, int], list[int]] = {}
    current_improve = 0

    for line in text.split("\n"):
        # Section header: ## 參數 N: ...
        hdr = re.match(r"##\s*參數\s*(\d+)", line)
        if hdr:
            current_improve = int(hdr.group(1))
            continue

        if current_improve == 0:
            continue

        # Table row: | N 名稱 (EN) | 原理1, 原理2, ... |
        row = re.match(r"\|\s*(\d+)\s+.+?\|\s*([\d,\s]+)\s*\|", line)
        if row:
            worsen = int(row.group(1))
            principles = [int(x.strip()) for x in row.group(2).split(",") if x.strip()]
            matrix[(current_improve, worsen)] = principles

    return matrix


def _parse_40_principles(text: str) -> dict[int, TrizPrinciple]:
    """Parse 03_40_principles.md."""
    principles: dict[int, TrizPrinciple] = {}

    # Split by principle headers
    sections = re.split(r"###\s*#(\d+)\s+(.+?)(?:\n|$)", text)
    # sections: [preamble, id1, title1, body1, id2, title2, body2, ...]
    i = 1
    while i + 2 < len(sections):
        pid = int(sections[i])
        raw_title = sections[i + 1].strip()
        body = sections[i + 2]

        # Parse title: "分割 (Segmentation)"
        title_match = re.match(r"(.+?)\s*\((.+?)\)", raw_title)
        name_zh = title_match.group(1).strip() if title_match else raw_title
        name_en = title_match.group(2).strip() if title_match else ""

        # Sub-principles: lines starting with -
        sub_principles = []
        hint = ""
        for bline in body.split("\n"):
            bline = bline.strip()
            if bline.startswith("- **工程提示**"):
                hint = bline.replace("- **工程提示**：", "").replace("- **工程提示**:", "").strip()
            elif bline.startswith("- "):
                sub_principles.append(bline[2:])

        principles[pid] = TrizPrinciple(
            id=pid,
            name_zh=name_zh,
            name_en=name_en,
            sub_principles=sub_principles,
            engineering_hint=hint,
        )
        i += 3

    return principles


def _parse_separation_principles(text: str) -> list[SeparationPrinciple]:
    """Parse 04_separation_principles.md."""
    separations: list[SeparationPrinciple] = []

    # Split by ### N. headers
    sections = re.split(r"###\s*(\d+)\.\s+(.+?)(?:\n|$)", text)
    i = 1
    while i + 2 < len(sections):
        sid = int(sections[i])
        raw_title = sections[i + 1].strip()
        body = sections[i + 2]

        title_match = re.match(r"(.+?)\s*\((.+?)\)", raw_title)
        name_zh = title_match.group(1).strip() if title_match else raw_title
        name_en = title_match.group(2).strip() if title_match else ""

        # Core question
        cq_match = re.search(r"\*\*核心問題\*\*[：:]\s*(.+)", body)
        core_question = cq_match.group(1).strip() if cq_match else ""

        # Strategies from table rows
        strategies: list[SeparationStrategy] = []
        for row in re.finditer(
            r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|", body
        ):
            s, d, e = row.group(1).strip(), row.group(2).strip(), row.group(3).strip()
            if s in ("策略", "---", "------"):
                continue
            strategies.append(SeparationStrategy(strategy=s, description=d, example=e))

        # Applicability hint
        ah_match = re.search(r"\*\*適用判斷\*\*[：:]\s*(.+)", body)
        applicability = ah_match.group(1).strip() if ah_match else ""

        separations.append(SeparationPrinciple(
            id=sid,
            name_zh=name_zh,
            name_en=name_en,
            core_question=core_question,
            strategies=strategies,
            applicability_hint=applicability,
        ))
        i += 3

    return separations


def _parse_76_standards(text: str) -> list[StandardSolution]:
    """Parse 05_76_standard_solutions.md."""
    standards: list[StandardSolution] = []

    # Split by #### N.N.N headers
    sections = re.split(r"####\s+([\d.]+)\s+(.+?)(?:\n|$)", text)
    i = 1
    while i + 2 < len(sections):
        code = sections[i].strip()
        name_zh = sections[i + 1].strip()
        body = sections[i + 2]

        # Bold description line
        desc_match = re.search(r"\*\*(.+?)\*\*", body)
        description = desc_match.group(1).strip() if desc_match else ""

        # Example: > ... line
        example_lines = [ln.strip()[1:].strip() for ln in body.split("\n") if ln.strip().startswith(">")]
        example = " ".join(example_lines)

        standards.append(StandardSolution(
            code=code,
            name_zh=name_zh,
            description=description,
            example=example,
        ))
        i += 3

    return standards


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class TrizEngine:
    """Deterministic TRIZ rule engine. Stateless after init."""

    def __init__(self, kb_path: Path):
        text_params = (kb_path / "01_39_parameters.md").read_text(encoding="utf-8")
        text_matrix = (kb_path / "02_contradiction_matrix.md").read_text(encoding="utf-8")
        text_principles = (kb_path / "03_40_principles.md").read_text(encoding="utf-8")
        text_separation = (kb_path / "04_separation_principles.md").read_text(encoding="utf-8")
        text_standards = (kb_path / "05_76_standard_solutions.md").read_text(encoding="utf-8")

        self.params = _parse_39_parameters(text_params)
        self.mapping_hints = _parse_mapping_hints(text_params)
        self.matrix = _parse_contradiction_matrix(text_matrix)
        self.principles = _parse_40_principles(text_principles)
        self.separations = _parse_separation_principles(text_separation)
        self.standards = _parse_76_standards(text_standards)

    # -- Lookups --

    def lookup_matrix(self, improve_id: int, worsen_id: int) -> list[int]:
        """Return recommended principle numbers from contradiction matrix."""
        return self.matrix.get((improve_id, worsen_id), [])

    def get_principles(self, ids: list[int]) -> list[TrizPrinciple]:
        """Return principle details for given IDs."""
        return [self.principles[pid] for pid in ids if pid in self.principles]

    def get_standards_for_state(self, sufield_state: str) -> list[StandardSolution]:
        """Return applicable standard solutions for a Su-Field state."""
        prefixes = SUFIELD_STATE_CLASSES.get(sufield_state, [])
        return [s for s in self.standards if any(s.code.startswith(p) for p in prefixes)]

    # -- Prompt formatters --

    def format_params_for_prompt(self) -> str:
        """Format 39 params as table for LLM injection."""
        lines = ["| # | 參數名稱 | 英文 | 常見工程對應 |", "|---|---------|------|-------------|"]
        for pid in sorted(self.params):
            p = self.params[pid]
            lines.append(f"| {p.id} | {p.name_zh} | {p.name_en} | {p.engineering_hints} |")
        return "\n".join(lines)

    def format_principles_for_prompt(self, ids: list[int]) -> str:
        """Format selected principles with details."""
        parts = []
        for pid in ids:
            p = self.principles.get(pid)
            if not p:
                continue
            sub = "\n".join(f"  - {s}" for s in p.sub_principles)
            parts.append(
                f"### #{p.id} {p.name_zh} ({p.name_en})\n"
                f"{sub}\n"
                f"  工程提示：{p.engineering_hint}"
            )
        return "\n\n".join(parts)

    def format_separations_for_prompt(self) -> str:
        """Format all 4 separation principles."""
        parts = []
        for sep in self.separations:
            strategies = "\n".join(
                f"  - {s.strategy}：{s.description}（{s.example}）" for s in sep.strategies
            )
            parts.append(
                f"### {sep.id}. {sep.name_zh} ({sep.name_en})\n"
                f"核心問題：{sep.core_question}\n"
                f"{strategies}\n"
                f"適用判斷：{sep.applicability_hint}"
            )
        return "\n\n".join(parts)

    def format_standards_for_prompt(self, standards: list[StandardSolution]) -> str:
        """Format selected standard solutions."""
        parts = []
        for s in standards:
            parts.append(f"#### {s.code} {s.name_zh}\n{s.description}\n範例：{s.example}")
        return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

KB_PATH = Path(__file__).parent.parent.parent / "rd_assistant_design_system" / "triz_knowledge_base"
triz_engine = TrizEngine(KB_PATH)
