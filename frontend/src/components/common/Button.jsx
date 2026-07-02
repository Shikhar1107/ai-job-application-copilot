export default function Button({
    children,
    type = "button",
    variant = "primary",
    disabled = false,
    onClick,
    className= "",
}) {
    const baseStyles = " inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-60";

    const variants = {
        primary: "bg-slate-900 text-white hover:bg-slate-800",
        secondary: "bg-white text-slate-900 border border-slate-300 hover:bg-slate-50",
        outline: "border border-slate-300 text-slate-700 hover:bg-slate-100",
        danger: "bg-red-600 text-white hover:bg-red-700",
    };

    return(
        <button
        type = {type}
        disabled = {disabled}
        onClick={onClick}
        className={`${baseStyles} ${variants[variant]} ${className}`}
        >
            {children}
        </button>
    );

}