export default function Logo({ className = "" }: { className?: string }) {
  return (
    <span className={`inline-flex items-center gap-2 ${className}`}>
      <svg width="26" height="26" viewBox="0 0 40 40" fill="none" aria-hidden>
        <defs>
          <linearGradient id="cayba-roof" x1="6" y1="32" x2="34" y2="6" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#E8452F" />
            <stop offset="100%" stopColor="#FF8A63" />
          </linearGradient>
        </defs>
        <path
          d="M20 6 L34 32 L6 32 Z"
          fill="none"
          stroke="url(#cayba-roof)"
          strokeWidth="3.4"
          strokeLinejoin="round"
          strokeLinecap="round"
        />
      </svg>
      <span className="font-heading text-xl font-extrabold tracking-tight text-white">CAYBA</span>
    </span>
  )
}
