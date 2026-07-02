import { Upload } from "lucide-react";
import Button from "../common/Button";

export default function ResumeUploader({
    resumeText,
    setResumeText,
    onFileUpload,
    isParsingResume,
}) {
    return (
    <div className="space-y-4">
        <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
                Upload Resume
            </label>
            <div className="rounded-xl border birder-dashed border-slate-300 bg-slate-50 p-5">
                <div className="flex flex-col items-center justify-center gap-3 text-center">
                    <div className="rounded-full bg-white p-3 text-slate-700 shadow-sm">
                        <Upload size={22} />
                    </div>

                <div>
                    <p className="text-sm font-medium text-slate-800">
                        Upload PDF, DOCX or TXT resume
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                        The backend will extract the text and fill the resume box below.
                    </p>
                </div>

                <input 
                type="file"
                accept= ".pdf,.docx,.txt"
                onChange={(event) => {
                    const file = event.target.files?.[0];
                    if(file) {
                        onFileUpload(file);
                    }
                }}
                disabled={isParsingResume}
                className="block w-full max-w-xs text-sm text-600 file:mr-4 file:rounded-lg file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-slate-800 disabled:opacity-60"
                />
                {isParsingResume && (
                    <p className="text-xs text-slate-500">
                        Extracting resume text...
                    </p>
                )}
                </div>
            </div>
        </div>

        <div>
            <label className="wb-2 block text-sm font-medium text-slate-700">
                Resume Text
            </label>
            
            <textarea value={resumeText} 
            onChange={(event) => setResumeText(event.target.value)}
            placeholder="Paste your resume text here, or upload a file above..."
            rows={12}
            className = "w-full rounded-xl border border-slate-300 bg-white p-4 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-slate-900 focus:ring-slate-200"
            />

            <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
                <span>
                    You can edit the extracted text before running analysis.
                </span>
                <span>{resumeText.length} characters</span>
            </div>
        </div>

        {resumeText && (
            <Button
            variant="outline"
            onClick={() => setResumeText("")}
            className="w-full"
            >
                Clear Resume Text
            </Button>
        )}
    </div>
    );
}