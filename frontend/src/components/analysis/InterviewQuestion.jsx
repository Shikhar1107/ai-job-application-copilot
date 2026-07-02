import { MessageCircleQuestion } from "lucide-react";
import Button from "../common/Button";
import Card from "../common/Card";
import Loader from "../common/Loader";
import ErrorMessage from "../common/ErrorMessage";

export default function InterviewQuestionsPanel({
  questions = [],
  onGenerate,
  isLoading,
  error,
  showGenerateButton = true,
}) {
  return (
    <Card className="space-y-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h3 className="text-base font-semibold text-slate-900">
            Interview Preparation
          </h3>
          <p className="mt-1 text-sm text-slate-500">
            Generate likely interview questions with suggested answers.
          </p>
        </div>
        {showGenerateButton && (
        <Button
          variant="secondary"
          onClick={onGenerate}
          disabled={isLoading}
          className="gap-2"
        >
          <MessageCircleQuestion size={16} />
          Generate Questions
        </Button>
        )}
      </div>

      <ErrorMessage message={error} />

      {isLoading && (
        <Loader message="Generating interview questions. This may take a few seconds..." />
      )}

      {!isLoading && questions.length === 0 && (
        <p className="rounded-lg bg-slate-50 p-4 text-sm text-slate-500">
          No interview questions generated yet.
        </p>
      )}

      {!isLoading && questions.length > 0 && (
        <div className="space-y-4">
          {questions.map((item, index) => (
            <div
              key={`${item.question}-${index}`}
              className="rounded-xl border border-slate-200 bg-slate-50 p-4"
            >
              <div className="mb-3 flex flex-wrap gap-2">
                {item.category && (
                  <span className="rounded-full bg-white px-3 py-1 text-xs font-medium text-slate-700 ring-1 ring-slate-200">
                    {item.category}
                  </span>
                )}

                {item.difficulty && (
                  <span className="rounded-full bg-white px-3 py-1 text-xs font-medium text-slate-700 ring-1 ring-slate-200">
                    {item.difficulty}
                  </span>
                )}
              </div>

              <div className="space-y-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Question
                  </p>
                  <p className="mt-1 text-sm font-semibold leading-6 text-slate-900">
                    {item.question}
                  </p>
                </div>

                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Suggested Answer
                  </p>
                  <p className="mt-1 text-sm leading-6 text-slate-700">
                    {item.answer}
                  </p>
                </div>

                {item.evaluation_focus && (
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Evaluation Focus
                    </p>
                    <p className="mt-1 text-sm leading-6 text-slate-600">
                      {item.evaluation_focus}
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}