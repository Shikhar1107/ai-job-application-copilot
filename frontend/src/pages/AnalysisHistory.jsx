import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Clock, Eye } from "lucide-react";

import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Loader from "../components/common/Loader";
import ErrorMessage from "../components/common/ErrorMessage";
import { getAnalysisHistory } from "../api/historyApi";

function formatDate(value) {
  if (!value) return "Unknown date";

  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function getFitLabel(score) {
  if (score >= 80) return "Strong Match";
  if (score >= 60) return "Good Match";
  if (score >= 40) return "Partial Match";
  return "Low Match";
}

export default function AnalysisHistory() {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadHistory() {
    setError("");
    setIsLoading(true);

    try {
      const data = await getAnalysisHistory();
      setHistory(data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">
            Analysis History
          </h2>
          <p className="mt-1 text-sm text-slate-600">
            View previous resume-job analyses saved in PostgreSQL.
          </p>
        </div>

        <Button variant="secondary" onClick={loadHistory} disabled={isLoading}>
          Refresh
        </Button>
      </section>

      <ErrorMessage message={error} />

      {isLoading && <Loader message="Loading saved analyses..." />}

      {!isLoading && history.length === 0 && (
        <Card>
          <div className="py-10 text-center">
            <p className="text-sm font-medium text-slate-700">
              No saved analyses yet.
            </p>
            <p className="mt-1 text-sm text-slate-500">
              Run your first resume-job analysis to see it here.
            </p>

            <Link to="/analyze" className="mt-4 inline-block">
              <Button>Analyze Resume</Button>
            </Link>
          </div>
        </Card>
      )}

      {!isLoading && history.length > 0 && (
        <div className="space-y-4">
          {history.map((item) => (
            <Card key={item.id}>
              <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
                <div className="flex-1 space-y-3">
                  <div className="flex flex-wrap items-center gap-3">
                    <span className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">
                      {item.fit_score}/100
                    </span>

                    <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-700">
                      {getFitLabel(item.fit_score)}
                    </span>

                    <span className="inline-flex items-center gap-1 text-xs text-slate-500">
                      <Clock size={14} />
                      {formatDate(item.created_at)}
                    </span>
                  </div>

                  <p className="line-clamp-3 text-sm leading-6 text-slate-700">
                    {item.fit_summary}
                  </p>

                  <div className="grid gap-3 md:grid-cols-2">
                    <div>
                      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
                        Matched Skills
                      </p>

                      <div className="flex flex-wrap gap-2">
                        {(item.matched_skills || []).slice(0, 6).map((skill) => (
                          <span
                            key={skill}
                            className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700 ring-1 ring-emerald-200"
                          >
                            {skill}
                          </span>
                        ))}

                        {(item.matched_skills || []).length > 6 && (
                          <span className="rounded-full bg-slate-50 px-3 py-1 text-xs font-medium text-slate-500 ring-1 ring-slate-200">
                            +{item.matched_skills.length - 6} more
                          </span>
                        )}
                      </div>
                    </div>

                    <div>
                      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
                        Missing Skills
                      </p>

                      <div className="flex flex-wrap gap-2">
                        {(item.missing_skills || []).slice(0, 6).map((skill) => (
                          <span
                            key={skill}
                            className="rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700 ring-1 ring-amber-200"
                          >
                            {skill}
                          </span>
                        ))}

                        {(item.missing_skills || []).length > 6 && (
                          <span className="rounded-full bg-slate-50 px-3 py-1 text-xs font-medium text-slate-500 ring-1 ring-slate-200">
                            +{item.missing_skills.length - 6} more
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                <Link to={`/history/${item.id}`}>
                  <Button variant="outline" className="gap-2">
                    <Eye size={16} />
                    View Details
                  </Button>
                </Link>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}