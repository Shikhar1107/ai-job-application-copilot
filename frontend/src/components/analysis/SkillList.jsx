export default function SkillList({ title, skills = [], emptyText = "No skills found." }) {
  return (
    <div>
      <h3 className="mb-3 text-sm font-semibold text-slate-900">
        {title}
      </h3>

      {skills.length === 0 ? (
        <p className="text-sm text-slate-500">{emptyText}</p>
      ) : (
        <div className="flex flex-wrap gap-2">
          {skills.map((skill) => (
            <span
              key={skill}
              className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-700"
            >
              {skill}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}