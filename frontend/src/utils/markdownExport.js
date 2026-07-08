function listToMarkdown(items = []) {
  if (!items || items.length === 0) {
    return "- None";
  }

  return items.map((item) => `- ${item}`).join("\n");
}

function rewrittenBulletsToMarkdown(bullets = []) {
  if (!bullets || bullets.length === 0) {
    return "_No rewritten bullets generated._";
  }

  return bullets
    .map((item, index) => {
      return [
        `### Bullet ${index + 1}`,
        "",
        `**Original:** ${item.original_bullet || "N/A"}`,
        "",
        `**Rewritten:** ${item.rewritten_bullet || "N/A"}`,
        "",
        `**Reason:** ${item.reason || "N/A"}`,
      ].join("\n");
    })
    .join("\n\n");
}

function interviewQuestionsToMarkdown(questions = []) {
  if (!questions || questions.length === 0) {
    return "_No interview questions generated._";
  }

  return questions
    .map((item, index) => {
      return [
        `### Question ${index + 1}: ${item.question || "N/A"}`,
        "",
        `**Category:** ${item.category || "N/A"}`,
        "",
        `**Difficulty:** ${item.difficulty || "N/A"}`,
        "",
        `**Suggested Answer:**`,
        "",
        item.answer || "N/A",
        "",
        `**Evaluation Focus:** ${item.evaluation_focus || "N/A"}`,
      ].join("\n");
    })
    .join("\n\n");
}

function safeText(value) {
  return value && String(value).trim() ? String(value).trim() : "N/A";
}

export function buildAnalysisMarkdown(analysis) {
  const createdAt = analysis.created_at
    ? new Date(analysis.created_at).toLocaleString("en-IN")
    : "N/A";

  return [
    `# AI Job Application Analysis`,
    "",
    `**Analysis ID:** ${analysis.id || analysis.analysis_id || "N/A"}`,
    "",
    `**Created At:** ${createdAt}`,
    "",
    `**Fit Score:** ${analysis.fit_score ?? "N/A"}/100`,
    "",
    `## Fit Summary`,
    "",
    safeText(analysis.fit_summary),
    "",
    `## Matched Skills`,
    "",
    listToMarkdown(analysis.matched_skills),
    "",
    `## Missing Skills`,
    "",
    listToMarkdown(analysis.missing_skills),
    "",
    `## Resume Skills`,
    "",
    listToMarkdown(analysis.resume_skills),
    "",
    `## Job Required Skills`,
    "",
    listToMarkdown(analysis.job_required_skills),
    "",
    `## Tailored Resume Bullets`,
    "",
    rewrittenBulletsToMarkdown(analysis.rewritten_bullets),
    "",
    `## Cover Letter`,
    "",
    safeText(analysis.cover_letter),
    "",
    `## Interview Preparation Questions`,
    "",
    interviewQuestionsToMarkdown(analysis.interview_questions),
    "",
    `---`,
    "",
    `## Original Resume Text`,
    "",
    "```txt",
    safeText(analysis.resume_text),
    "```",
    "",
    `## Original Job Description`,
    "",
    "```txt",
    safeText(analysis.job_description),
    "```",
  ].join("\n");
}

export function downloadMarkdownFile(content, filename) {
  const blob = new Blob([content], {
    type: "text/markdown;charset=utf-8",
  });

  const url = URL.createObjectURL(blob);

  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();

  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
}

export function getAnalysisMarkdownFilename(analysis) {
  const id = analysis.id || analysis.analysis_id || "analysis";

  const date = analysis.created_at
    ? new Date(analysis.created_at).toISOString().slice(0, 10)
    : new Date().toISOString().slice(0, 10);

  return `job-analysis-${id}-${date}.md`;
}