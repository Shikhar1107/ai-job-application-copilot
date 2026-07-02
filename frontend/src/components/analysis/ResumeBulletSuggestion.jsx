import { FileText } from "lucide-react";
import Button from "../common/Button";
import Card from "../common/Card";
import Loader from "../common/Loader";
import ErrorMessage from "../common/ErrorMessage";

export default function ResumeBulletSuggestions({
  bullets = [],
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
            Tailored Resume Bullets
          </h3>
          <p className="mt-1 text-sm text-slate-500">
            Rewrite resume bullets to better align with the job description.
          </p>
        </div>
        {showGenerateButton && (
        <Button
          variant="secondary"
          onClick={onGenerate}
          disabled={isLoading}
          className="gap-2"
        >
          <FileText size={16} />
          Generate Bullets
        </Button>
        )}
      </div>

      <ErrorMessage message={error} />

      {isLoading && (
        <Loader message="Generating tailored resume bullets. This may take a few seconds..." />
      )}

      {!isLoading && bullets.length === 0 && (
        <p className="rounded-lg bg-slate-50 p-4 text-sm text-slate-500">
          No rewritten bullets generated yet.
        </p>
      )}

      {!isLoading && bullets.length > 0 && (
        <div className="space-y-4">
          {bullets.map((item, index) => (
            <div
              key={`${item.original_bullet}-${index}`}
              className="rounded-xl border border-slate-200 bg-slate-50 p-4"
            >
              <div className="space-y-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Original
                  </p>
                  <p className="mt-1 text-sm leading-6 text-slate-700">
                    {item.original_bullet}
                  </p>
                </div>

                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Rewritten
                  </p>
                  <p className="mt-1 text-sm font-medium leading-6 text-slate-900">
                    {item.rewritten_bullet}
                  </p>
                </div>

                {item.reason && (
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Why this works
                    </p>
                    <p className="mt-1 text-sm leading-6 text-slate-600">
                      {item.reason}
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