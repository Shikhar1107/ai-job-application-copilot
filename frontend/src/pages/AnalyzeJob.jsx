import { useState } from "react";
import { Sparkles } from "lucide-react";

import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Loader from "../components/common/Loader";
import ErrorMessage from "../components/common/ErrorMessage";

import ResumeUploader from "../components/analysis/ResumeUploader";
import JobDescriptionInput from "../components/analysis/JobDescription";
import FitScoreCard from "../components/analysis/FitScoreCard";
import SkillList from "../components/analysis/SkillList";
import ResumeBulletSuggestions from "../components/analysis/ResumeBulletSuggestion";
import CoverLetterPanel from "../components/analysis/CoverLetterCard";
import InterviewQuestionsPanel from "../components/analysis/InterviewQuestion";

import { parseResume } from "../api/resumeApi";
import {
  analyzeResumeJob,
  generateResumeBullets,
  generateCoverLetter,
  generateInterviewQuestions,
} from "../api/analysisApi";

export default function AnalyzeJob() {

  const RESUME_MAX_CHARS = 8000;
  const JD_MAX_CHARS = 5000;
  const TOTAL_MAX_CHARS = 12000;

  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const [analysisResult, setAnalysisResult] = useState(null);

  const [rewrittenBullets, setRewrittenBullets] = useState([]);
  const [coverLetter, setCoverLetter] = useState("");
  const [interviewQuestions, setInterviewQuestions] = useState([]);

  const [isParsingResume, setIsParsingResume] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGeneratingBullets, setIsGeneratingBullets] = useState(false);
  const [isGeneratingCoverLetter, setIsGeneratingCoverLetter] = useState(false);
  const [isGeneratingQuestions, setIsGeneratingQuestions] = useState(false);

  const [error, setError] = useState("");
  const [resumeParseMessage, setResumeParseMessage] = useState("");

  const [bulletsError, setBulletsError] = useState("");
  const [coverLetterError, setCoverLetterError] = useState("");
  const [questionsError, setQuestionsError] = useState("");

  const resumeCharCount = resumeText.length;
  const jdCharCount = jobDescription.length;
  const totalCharCount = resumeCharCount + jdCharCount;

  const isResumeOverLimit = resumeCharCount > RESUME_MAX_CHARS;
  const isJdOverLimit = jdCharCount > JD_MAX_CHARS;
  const isTotalOverLimit = totalCharCount > TOTAL_MAX_CHARS;

  const isLargeInput = isResumeOverLimit || isJdOverLimit || isTotalOverLimit;

  async function handleResumeUpload(file) {
    setError("");
    setResumeParseMessage("");
    setIsParsingResume(true);

    try {
      const parsedResume = await parseResume(file);

      setResumeText(parsedResume.extracted_text || "");
      setResumeParseMessage(
        parsedResume.message || "Resume parsed successfully."
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setIsParsingResume(false);
    }
  }

  async function handleAnalyze() {
    setError("");
    setAnalysisResult(null);

    setRewrittenBullets([]);
    setCoverLetter("");
    setInterviewQuestions([]);

    setBulletsError("");
    setCoverLetterError("");
    setQuestionsError("");

    if (!resumeText.trim()) {
      setError("Please upload or paste your resume text.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please paste the job description.");
      return;
    }

    setIsAnalyzing(true);

    try {
      const result = await analyzeResumeJob({
        resume_text: resumeText,
        job_description: jobDescription,
      });

      setAnalysisResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsAnalyzing(false);
    }
  }

  async function handleGenerateBullets() {
    if (!analysisResult) return;

    setBulletsError("");
    setIsGeneratingBullets(true);

    try {
      const result = await generateResumeBullets({
        analysis_id: analysisResult.analysis_id,
        resume_text: resumeText,
        job_description: jobDescription,
        matched_skills: analysisResult.matched_skills || [],
        missing_skills: analysisResult.missing_skills || [],
      });

      setRewrittenBullets(result.rewritten_bullets || []);
    } catch (err) {
      setBulletsError(err.message);
    } finally {
      setIsGeneratingBullets(false);
    }
  }

  async function handleGenerateCoverLetter() {
    if (!analysisResult) return;

    setCoverLetterError("");
    setIsGeneratingCoverLetter(true);

    try {
      const result = await generateCoverLetter({
        analysis_id: analysisResult.analysis_id,
        resume_text: resumeText,
        job_description: jobDescription,
        fit_score: analysisResult.fit_score,
        fit_summary: analysisResult.fit_summary,
        matched_skills: analysisResult.matched_skills || [],
        missing_skills: analysisResult.missing_skills || [],
        // rewritten_bullets: rewrittenBullets || [],
      });

      setCoverLetter(result.cover_letter || "");
    } catch (err) {
      setCoverLetterError(err.message);
    } finally {
      setIsGeneratingCoverLetter(false);
    }
  }

  async function handleGenerateQuestions() {
    if (!analysisResult) return;

    setQuestionsError("");
    setIsGeneratingQuestions(true);

    try {
      const result = await generateInterviewQuestions({
        resume_text: resumeText,
        job_description: jobDescription,
        fit_score: analysisResult.fit_score,
        fit_summary: analysisResult.fit_summary,
        matched_skills: analysisResult.matched_skills || [],
        missing_skills: analysisResult.missing_skills || [],
      });

      setInterviewQuestions(result.interview_questions || []);
    } catch (err) {
      setQuestionsError(err.message);
    } finally {
      setIsGeneratingQuestions(false);
    }
  }

  const isAnalyzeDisabled =
    isAnalyzing ||
    isParsingResume ||
    !resumeText.trim() ||
    !jobDescription.trim();

  return (
    <div className="space-y-8">
      <section className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">
            Analyze Resume Against Job Description
          </h2>
          <p className="mt-1 max-w-2xl text-sm text-slate-600">
            Upload or paste your resume, paste a job description, and get a
            skill match breakdown with an explainable fit score.
          </p>
        </div>
        <div className="rounded-xl border bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h3 className="text-sm font-semibold text-slate-800">
                Input Size Limits
              </h3>
              <p className="mt-1 text-xs text-slate-500">
                Recommended max: {TOTAL_MAX_CHARS.toLocaleString()} total characters
                for stable analysis on the deployed free model.
              </p>
            </div>

            {isLargeInput && (
              <span className="shrink-0 rounded-full bg-yellow-100 px-3 py-1 text-xs font-medium text-yellow-800">
                Over recommended limit
              </span>
            )}
          </div>

          <div className="mt-4 grid gap-3 text-sm md:grid-cols-3">
            <div
              className={`rounded-lg border p-3 ${
                isResumeOverLimit
                  ? "border-yellow-300 bg-yellow-50"
                  : "border-slate-200 bg-slate-50"
              }`}
            >
              <p className="font-medium text-slate-700">Resume</p>
              <p className="mt-1 text-slate-600">
                {resumeCharCount.toLocaleString()} /{" "}
                {RESUME_MAX_CHARS.toLocaleString()} characters
              </p>
            </div>

            <div
              className={`rounded-lg border p-3 ${
                isJdOverLimit
                  ? "border-yellow-300 bg-yellow-50"
                  : "border-slate-200 bg-slate-50"
              }`}
            >
              <p className="font-medium text-slate-700">Job Description</p>
              <p className="mt-1 text-slate-600">
                {jdCharCount.toLocaleString()} / {JD_MAX_CHARS.toLocaleString()}{" "}
                characters
              </p>
            </div>

            <div
              className={`rounded-lg border p-3 ${
                isTotalOverLimit
                  ? "border-yellow-300 bg-yellow-50"
                  : "border-slate-200 bg-slate-50"
              }`}
            >
              <p className="font-medium text-slate-700">Total Input</p>
              <p className="mt-1 text-slate-600">
                {totalCharCount.toLocaleString()} /{" "}
                {TOTAL_MAX_CHARS.toLocaleString()} characters
              </p>
            </div>
          </div>

          {isLargeInput && (
            <p className="mt-3 text-sm text-yellow-700">
              This input is above the recommended limit for the deployed free model.
              The analysis may be slower or may fail. For best results, shorten the
              resume or job description before running analysis.
            </p>
          )}
        </div>

        <Button
          onClick={handleAnalyze}
          disabled={isAnalyzeDisabled}
          className="gap-2"
        >
          <Sparkles size={16} />
          Analyze Fit
        </Button>
      </section>

      <ErrorMessage message={error} />

      {resumeParseMessage && (
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">
          {resumeParseMessage}
        </div>
      )}

      <section className="grid gap-6 lg:grid-cols-2">
        <Card>
          <ResumeUploader
            resumeText={resumeText}
            setResumeText={setResumeText}
            onFileUpload={handleResumeUpload}
            isParsingResume={isParsingResume}
          />
        </Card>

        <Card>
          <JobDescriptionInput
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
          />
        </Card>
      </section>

      {isAnalyzing && (
        <Loader message="Analyzing resume and job description. This can take 20–40 seconds depending on the LLM provider." />
      )}

      {analysisResult && (
        <section className="space-y-6">
          {analysisResult.id && (
            <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 text-sm text-blue-700">
              Analysis saved with ID #{analysisResult.analysis_id}. Optional generations will be saved to the same history record.
            </div>
          )}
          <FitScoreCard result={analysisResult} />

          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <SkillList
                title="Matched Skills"
                skills={analysisResult.matched_skills}
                emptyText="No matched skills found."
              />
            </Card>

            <Card>
              <SkillList
                title="Missing Skills"
                skills={analysisResult.missing_skills}
                emptyText="No missing skills found."
              />
            </Card>

            <Card>
              <SkillList
                title="Resume Skills"
                skills={analysisResult.resume_skills}
                emptyText="No resume skills extracted."
              />
            </Card>

            <Card>
              <SkillList
                title="Job Required Skills"
                skills={analysisResult.job_required_skills}
                emptyText="No job skills extracted."
              />
            </Card>
          </div>

          <div className="space-y-6">
            <ResumeBulletSuggestions
              bullets={rewrittenBullets}
              onGenerate={handleGenerateBullets}
              isLoading={isGeneratingBullets}
              error={bulletsError}
            />

            <CoverLetterPanel
              coverLetter={coverLetter}
              onGenerate={handleGenerateCoverLetter}
              isLoading={isGeneratingCoverLetter}
              error={coverLetterError}
            />

            <InterviewQuestionsPanel
              questions={interviewQuestions}
              onGenerate={handleGenerateQuestions}
              isLoading={isGeneratingQuestions}
              error={questionsError}
            />
          </div>
        </section>
      )}
    </div>
  );
}