import Card from "../common/Card";

function getFitLabel(score) {
  if (score >= 80) return "Strong Match";
  if (score >= 60) return "Good Match";
  if (score >= 40) return "Partial Match";
  return "Low Match";
}

export default function FitScoreCard({ result }) {
  if (!result) return null;

  const score = result.fit_score ?? 0;
  const label = getFitLabel(score);

  return (
    <Card className="space-y-5">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            Resume-Job Fit Score
          </p>
          <h2 className="mt-1 text-3xl font-bold text-slate-900">
            {score}/100
          </h2>
          <p className="mt-1 text-sm font-medium text-slate-700">
            {label}
          </p>
        </div>

        <div className="h-24 w-24 rounded-full border-8 border-slate-900 bg-white p-2">
          <div className="flex h-full w-full items-center justify-center rounded-full bg-slate-50">
            <span className="text-xl font-bold text-slate-900">
              {score}%
            </span>
          </div>
        </div>
      </div>

      <div>
        <h3 className="mb-2 text-sm font-semibold text-slate-900">
          Fit Summary
        </h3>
        <p className="text-sm leading-6 text-slate-700">
          {result.fit_summary}
        </p>
      </div>
    </Card>
  );
}