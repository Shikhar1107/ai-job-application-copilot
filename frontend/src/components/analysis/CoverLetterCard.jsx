import { Mail, Copy } from "lucide-react";
import Button from "../common/Button";
import Card from "../common/Card";
import Loader from "../common/Loader";
import ErrorMessage from "../common/ErrorMessage";

export default function CoverLetterPanel({
  coverLetter,
  onGenerate,
  isLoading,
  error,
  showGenerateButton = true,
}) {
  async function handleCopy() {
    if (!coverLetter) return;
    await navigator.clipboard.writeText(coverLetter);
  }

  return (
    <Card className="space-y-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h3 className="text-base font-semibold text-slate-900">
            Cover Letter
          </h3>
          <p className="mt-1 text-sm text-slate-500">
            Generate a grounded cover letter based on the resume-job fit.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          {coverLetter && (
            <Button
              variant="outline"
              onClick={handleCopy}
              disabled={isLoading}
              className="gap-2"
            >
              <Copy size={16} />
              Copy
            </Button>
          )}
          {showGenerateButton && (
          <Button
            variant="secondary"
            onClick={onGenerate}
            disabled={isLoading}
            className="gap-2"
          >
            <Mail size={16} />
            Generate Cover Letter
          </Button>
          )}
        </div>
      </div>

      <ErrorMessage message={error} />

      {isLoading && (
        <Loader message="Generating cover letter. This may take a few seconds..." />
      )}

      {!isLoading && !coverLetter && (
        <p className="rounded-lg bg-slate-50 p-4 text-sm text-slate-500">
          No cover letter generated yet.
        </p>
      )}

      {!isLoading && coverLetter && (
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
          <pre className="whitespace-pre-wrap font-sans text-sm leading-7 text-slate-800">
            {coverLetter}
          </pre>
        </div>
      )}
    </Card>
  );
}