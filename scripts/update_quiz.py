#!/usr/bin/env python3
"""
自动扫描 docs/note/*/quiz.yml，校验题目 schema，
生成 docs/quiz/index.md（总览卡片）和 docs/quiz/<subject>.md（分科目页面）。
"""

from __future__ import annotations

import base64
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# 尝试导入 PyYAML，若未安装则给出友好提示
try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML 未安装，请运行: uv add pyyaml 或 pip install pyyaml"
    ) from exc

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
NOTE_ROOT = DOCS / "note"
QUIZ_ROOT = DOCS / "quiz"

MARKER_BEGIN = "<!-- quiz:auto-begin -->"
MARKER_END = "<!-- quiz:auto-end -->"

VALID_TYPES = {"single_choice", "multiple_choice", "true_false", "fill_blank", "short_answer"}
VALID_DIFFICULTIES = {"core", "advanced", "exam"}


@dataclass
class Question:
    id: str
    type: str
    difficulty: str
    question: str
    options: list[str] = field(default_factory=list)
    answer: Any = None
    explanation: str = ""
    keywords: list[str] = field(default_factory=list)
    chapter: str = ""
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "difficulty": self.difficulty,
            "question": self.question,
            "answer": self.answer,
            "explanation": self.explanation,
            "chapter": self.chapter,
            "source": self.source,
        }
        if self.options:
            d["options"] = self.options
        if self.keywords:
            d["keywords"] = self.keywords
        return d


@dataclass
class QuizSubject:
    subject: str
    slug: str
    path: Path
    questions: list[Question] = field(default_factory=list)

    @property
    def question_count(self) -> int:
        return len(self.questions)

    def difficulty_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {"core": 0, "advanced": 0, "exam": 0}
        for q in self.questions:
            if q.difficulty in counts:
                counts[q.difficulty] += 1
        return counts

    def chapter_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for q in self.questions:
            counts[q.chapter] = counts.get(q.chapter, 0) + 1
        return counts


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _esc_json_for_html(text: str) -> str:
    """将字符串转义为可安全嵌入 HTML script 标签的 JSON 字符串。"""
    # 先用标准 JSON 转义，再将 </script> 相关字符做额外防护
    j = json.dumps(text, ensure_ascii=False)
    # 去掉 json.dumps 外层的双引号，对内容做 HTML 转义
    # 实际上我们直接对整个 JSON 块做 HTML 转义更安全
    return j


def load_yaml_quiz(path: Path) -> QuizSubject:
    """加载单个 quiz.yml 文件。"""
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise SystemExit(f"{path} 根节点不是字典")

    subject = str(data.get("subject", path.parent.name))
    slug = path.parent.name  # 目录名作为 slug
    quiz = QuizSubject(subject=subject, slug=slug, path=path)

    chapters = data.get("chapters", [])
    if not isinstance(chapters, list):
        raise SystemExit(f"{path} 中 chapters 不是列表")

    for ch in chapters:
        if not isinstance(ch, dict):
            continue
        chapter_name = str(ch.get("chapter", ""))
        source = str(ch.get("source", ""))
        questions = ch.get("questions", [])
        if not isinstance(questions, list):
            continue
        for q_raw in questions:
            if not isinstance(q_raw, dict):
                continue
            q = parse_question(q_raw, chapter_name, source, path)
            if q:
                quiz.questions.append(q)

    return quiz


def parse_question(raw: dict[str, Any], chapter: str, source: str, path: Path) -> Question | None:
    """解析单个题目，返回 Question 或 None（解析失败时打印警告）。"""
    qid = str(raw.get("id", "")).strip()
    qtype = str(raw.get("type", "")).strip()
    difficulty = str(raw.get("difficulty", "core")).strip()
    question_text = str(raw.get("question", "")).strip()
    answer = raw.get("answer")
    explanation = str(raw.get("explanation", "")).strip()
    keywords = raw.get("keywords", [])
    options = raw.get("options", [])

    warnings: list[str] = []

    if not qid:
        warnings.append("缺少 id")
    if not qtype:
        warnings.append("缺少 type")
    elif qtype not in VALID_TYPES:
        warnings.append(f"非法 type: {qtype}")
    if not question_text:
        warnings.append("缺少 question")
    if answer is None and qtype != "short_answer":
        warnings.append("缺少 answer")
    if difficulty not in VALID_DIFFICULTIES:
        warnings.append(f"非法 difficulty: {difficulty}，使用 core")
        difficulty = "core"

    if qtype in ("single_choice", "multiple_choice"):
        if not options or not isinstance(options, list):
            warnings.append("单选/多选缺少 options 数组")
        if qtype == "single_choice" and answer is not None:
            if not isinstance(answer, int) or answer < 0:
                warnings.append("单选 answer 应为非负整数索引")
        if qtype == "multiple_choice" and answer is not None:
            if not isinstance(answer, list) or not all(isinstance(a, int) for a in answer):
                warnings.append("多选 answer 应为整数索引数组")

    if qtype == "true_false" and answer is not None:
        if answer not in (True, False, "true", "false"):
            warnings.append("判断题 answer 应为 true/false")

    if qtype == "fill_blank" and answer is not None:
        if not isinstance(answer, (str, list)):
            warnings.append("填空题 answer 应为字符串或字符串数组")

    if warnings:
        print(f"  [警告] {path.name} 题目 {qid or '(无id)'}: {', '.join(warnings)}")
        # 有严重错误时跳过
        if "缺少 id" in warnings or "缺少 type" in warnings or "缺少 question" in warnings:
            return None

    return Question(
        id=qid or "unknown",
        type=qtype or "single_choice",
        difficulty=difficulty,
        question=question_text,
        options=list(options) if isinstance(options, list) else [],
        answer=answer,
        explanation=explanation,
        keywords=list(keywords) if isinstance(keywords, list) else [],
        chapter=chapter,
        source=source,
    )


def collect_quizzes() -> list[QuizSubject]:
    """扫描所有 quiz.yml 文件。"""
    quizzes: list[QuizSubject] = []
    for quiz_path in sorted(NOTE_ROOT.rglob("quiz.yml")):
        print(f"加载 {quiz_path.relative_to(REPO_ROOT)} ...")
        quiz = load_yaml_quiz(quiz_path)
        quizzes.append(quiz)
    return quizzes


def build_index_md(quizzes: list[QuizSubject]) -> str:
    """构建 quiz 总览页 Markdown。"""
    lines: list[str] = []
    lines.append("---")
    lines.append('title: "复习题库"')
    lines.append("comments: false")
    lines.append("---")
    lines.append("")
    lines.append("# 复习题库")
    lines.append("")
    lines.append("按科目选择复习内容，进入对应题库进行练习或测验。")
    lines.append("")
    lines.append(MARKER_BEGIN)
    lines.append('<div class="quiz-subject-grid">')

    for quiz in quizzes:
        if quiz.question_count == 0:
            continue
        href = f"{quiz.slug}/"
        diff = quiz.difficulty_counts()
        diff_parts = []
        if diff["core"]:
            diff_parts.append(f"核心 {diff['core']} 题")
        if diff["advanced"]:
            diff_parts.append(f"进阶 {diff['advanced']} 题")
        if diff["exam"]:
            diff_parts.append(f"真题 {diff['exam']} 题")
        diff_str = "，".join(diff_parts) if diff_parts else ""

        lines.append('  <div class="quiz-subject-card">')
        lines.append(f'    <a href="{href}" class="quiz-subject-link">')
        lines.append(f'      <h3 class="quiz-subject-title">{_esc(quiz.subject)}</h3>')
        lines.append(f'      <div class="quiz-subject-count">共 {quiz.question_count} 题</div>')
        if diff_str:
            lines.append(f'      <div class="quiz-subject-diff">{_esc(diff_str)}</div>')
        lines.append("    </a>")
        lines.append("  </div>")

    lines.append("</div>")
    lines.append(MARKER_END)
    lines.append("")
    return "\n".join(lines)


def build_subject_md(quiz: QuizSubject) -> str:
    """构建单个科目的 quiz 页面 Markdown。"""
    lines: list[str] = []
    lines.append("---")
    lines.append(f'title: "{quiz.subject} 复习题库"')
    lines.append("comments: false")
    lines.append("---")
    lines.append("")
    lines.append(f"# {quiz.subject} 复习题库")
    lines.append("")
    lines.append("<div id=\"quiz-controls\">")
    lines.append('  <button id="quiz-mode-practice" class="quiz-btn active">练习模式</button>')
    lines.append('  <button id="quiz-mode-test" class="quiz-btn">测验模式</button>')
    lines.append('  <select id="quiz-chapter-filter">')
    lines.append('    <option value="">全部章节</option>')
    for ch in sorted(quiz.chapter_counts().keys()):
        lines.append(f'    <option value="{_esc(ch)}">{_esc(ch)}</option>')
    lines.append("  </select>")
    lines.append('  <label class="quiz-shuffle-toggle">')
    lines.append('    <input type="checkbox" id="quiz-shuffle">')
    lines.append('    <span>乱序选项</span>')
    lines.append('  </label>')
    lines.append("</div>")
    lines.append("")
    lines.append('<div id="quiz-progress"></div>')
    lines.append('<div id="quiz-app"></div>')
    lines.append("")
    lines.append(MARKER_BEGIN)

    # 嵌入 JSON 数据（使用 base64 避免 Markdown 对反斜杠的转义处理）
    questions_data = [q.to_dict() for q in quiz.questions]
    json_str = json.dumps(questions_data, ensure_ascii=False, indent=2)
    b64_json = base64.b64encode(json_str.encode("utf-8")).decode("ascii")
    lines.append('<script type="application/json" id="quiz-data" data-encoding="base64">')
    lines.append(b64_json)
    lines.append("</script>")
    lines.append(MARKER_END)
    lines.append("")
    return "\n".join(lines)


def inject_or_replace(content: str, block: str, marker_begin: str, marker_end: str) -> str:
    """在标记之间注入内容；若标记不存在则追加到末尾。"""
    pattern = re.compile(
        re.escape(marker_begin) + r"[\s\S]*?" + re.escape(marker_end),
        re.MULTILINE,
    )
    if pattern.search(content):
        replacement = f"{marker_begin}\n{block}\n{marker_end}"
        return pattern.sub(replacement, content, count=1)
    # 标记不存在，追加到末尾
    return content + "\n" + marker_begin + "\n" + block + "\n" + marker_end + "\n"


def write_index(quizzes: list[QuizSubject]) -> None:
    """生成总览页（始终全量覆盖）。"""
    index_path = QUIZ_ROOT / "index.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(build_index_md(quizzes), encoding="utf-8", newline="\n")
    print(f"已生成 {index_path.relative_to(REPO_ROOT)}")


def write_subject(quiz: QuizSubject) -> None:
    """生成分科目页面（始终全量覆盖）。"""
    subject_path = QUIZ_ROOT / f"{quiz.slug}.md"
    subject_path.parent.mkdir(parents=True, exist_ok=True)
    subject_path.write_text(build_subject_md(quiz), encoding="utf-8", newline="\n")
    print(f"已生成 {subject_path.relative_to(REPO_ROOT)}（{quiz.question_count} 题）")


def main() -> None:
    print("扫描题库数据...")
    quizzes = collect_quizzes()

    if not quizzes:
        print("未找到任何 quiz.yml 文件，退出。")
        sys.exit(1)

    total_questions = sum(q.question_count for q in quizzes)
    print(f"\n共发现 {len(quizzes)} 个科目，{total_questions} 道题目。")
    print("生成总览页...")
    write_index(quizzes)

    print("\n生成分科目页面...")
    for quiz in quizzes:
        write_subject(quiz)

    print("\n生成摘要:")
    for quiz in quizzes:
        diff = quiz.difficulty_counts()
        print(f"  - {quiz.subject}: {quiz.question_count} 题 "
              f"(核心 {diff['core']}, 进阶 {diff['advanced']}, 真题 {diff['exam']})")
    print(f"\nQuiz 页面生成完成！")


if __name__ == "__main__":
    main()
