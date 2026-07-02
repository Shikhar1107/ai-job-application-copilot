export default function JobDescriptionInput({
    jobDescription,
    setJobDescription,
}) {
    return (
        <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
                Job Descrpition
            </label>

            <textarea 
                value={jobDescription}
                onChange={(event) => setJobDescription(event.target.value)}
                placeholder="Paste the complete job description here..."
                rows={18}
                className="w-full rounded-xl border border-slate-300 bg-white p-4 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
            />

            <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
                <span>
                Include responsibilities, required skills, and preferred skills.
                </span>
                <span>{jobDescription.length} characters</span>
            </div>
        </div>
    );
}