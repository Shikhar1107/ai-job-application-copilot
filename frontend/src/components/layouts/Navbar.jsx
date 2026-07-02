import { NavLink } from "react-router-dom";
import { BriefcaseBusiness } from "lucide-react";

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `rounded-lg px-3 py-2 text-sm font-medium transition ${
      isActive
        ? "bg-slate-900 text-white"
        : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
    }`;

  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2">
          <div className="rounded-lg bg-slate-900 p-2 text-white">
            <BriefcaseBusiness size={20} />
          </div>

          <div>
            <h1 className="text-base font-semibold text-slate-900">
              AI Job Application Copilot
            </h1>
            <p className="text-xs text-slate-500">
              Resume-job fit analysis powered by GenAI
            </p>
          </div>
        </div>

        <nav className="flex items-center gap-2">
          <NavLink to="/analyze" className={linkClass}>
            Analyze
          </NavLink>
          <NavLink to="/history" className={linkClass}>
            History
          </NavLink>
        </nav>
      </div>
    </header>
  );
}