import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, Clock } from "lucide-react";

import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Loader from "../components/common/Loader";
import ErrorMessage from "../components/common/ErrorMessage";

import FitScoreCard from "../components/analysis/FitScoreCard";
import SkillList from "../components/analysis/SkillList";
import ResumeBulletSuggestions from "../components/analysis/ResumeBulletSuggestion";
import CoverLetterPanel from "../components/analysis/CoverLetterCard";
import InterviewQuestionsPanel from "../components/analysis/InterviewQuestion";

import { getAnalysisById } from "../api/historyApi";

function formatDate(value) {
  if (!value) return "Unknown date";

  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function TextPreview({ title, text }) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!text) {
    return (
      <Card>
        <h3 className="text-base font-semibold text-slate-900">{title}</h3>
        <p className="mt-3 text-sm text-slate-500">No text available.</p>
      </Card>
    );
  }

  const shouldClamp = text.length > 900;
  const visibleText = !shouldClamp || isExpanded ? text : `${text.slice(0, 900)}...`;

  return (
    <Card className="space-y-3">
      <h3 className="text-base font-semibold text-slate-900">{title}</h3>

      <pre className="whitespace-pre-wrap rounded-lg bg-slate-50 p-4 font-sans text-sm leading-7 text-slate-700">
        {visibleText}
      </pre>

      {shouldClamp && (
        <Button
          variant="outline"
          onClick={() => setIsExpanded((current) => !current)}
        >
          {isExpanded ? "Show Less" : "Show Full Text"}
        </Button>
      )}
    </Card>
  );
}

export default function AnalysisDetail() {
  const { id } = useParams();

  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadAnalysisDetail() {
    setError("");
    setIsLoading(true);

    try {
      const data = await getAnalysisById(id);
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadAnalysisDetail();
  }, [id]);

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <Link to="/history" className="mb-3 inline-block">
            <Button variant="outline" className="gap-2">
              <ArrowLeft size={16} />
              Back to History
            </Button>
          </Link>

          <h2 className="text-2xl font-bold text-slate-900">
            Analysis Detail
          </h2>

          <p className="mt-1 text-sm text-slate-600">
            Full saved analysis from PostgreSQL.
          </p>
        </div>

        {analysis?.created_at && (
          <div className="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600">
            <Clock size={16} />
            {formatDate(analysis.created_at)}
          </div>
        )}
      </section>

      <ErrorMessage message={error} />

      {isLoading && <Loader message="Loading analysis detail..." />}

      {!isLoading && !analysis && !error && (
        <Card>
          <div className="py-10 text-center">
            <p className="text-sm font-medium text-slate-700">
              Analysis not found.
            </p>
            <p className="mt-1 text-sm text-slate-500">
              The saved analysis may have been deleted or does not exist.
            </p>
          </div>
        </Card>
      )}

      {!isLoading && analysis && (
        <section className="space-y-6">
          <FitScoreCard result={analysis} />

          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <SkillList
                title="Matched Skills"
                skills={analysis.matched_skills}
                emptyText="No matched skills found."
              />
            </Card>

            <Card>
              <SkillList
                title="Missing Skills"
                skills={analysis.missing_skills}
                emptyText="No missing skills found."
              />
            </Card>

            <Card>
              <SkillList
                title="Resume Skills"
                skills={analysis.resume_skills}
                emptyText="No resume skills extracted."
              />
            </Card>

            <Card>
              <SkillList
                title="Job Required Skills"
                skills={analysis.job_required_skills}
                emptyText="No job skills extracted."
              />
            </Card>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <TextPreview title="Resume Text" text={analysis.resume_text} />
            <TextPreview title="Job Description" text={analysis.job_description} />
          </div>

          <ResumeBulletSuggestions
            bullets={analysis.rewritten_bullets || []}
            onGenerate={() => {}}
            isLoading={false}
            error=""
            showGenerateButton={false}
          />

          <CoverLetterPanel
            coverLetter={analysis.cover_letter || ""}
            onGenerate={() => {}}
            isLoading={false}
            error=""
            showGenerateButton={false}
          />

          <InterviewQuestionsPanel
            questions={analysis.interview_questions || []}
            onGenerate={() => {}}
            isLoading={false}
            error=""
            showGenerateButton={false}
          />
        </section>
      )}
    </div>
  );
}