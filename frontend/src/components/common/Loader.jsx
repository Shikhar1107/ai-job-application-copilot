export default function Loader({ message = "Loading..." }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
      <div className="flex items-center gap-3">
        <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-400 border-t-slate-900" />
        <span>{message}</span>
      </div>
    </div>
  );
}