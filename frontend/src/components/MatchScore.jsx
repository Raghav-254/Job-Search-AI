import { motion } from 'framer-motion';

const MatchScore = ({ score }) => {
  // Determine color based on score
  const getColor = () => {
    if (score >= 90) return { bg: 'bg-brand-500', text: 'text-brand-400', glow: 'shadow-brand-500/30' };
    if (score >= 70) return { bg: 'bg-emerald-500', text: 'text-emerald-400', glow: 'shadow-emerald-500/30' };
    if (score >= 50) return { bg: 'bg-amber-500', text: 'text-amber-400', glow: 'shadow-amber-500/30' };
    return { bg: 'bg-red-500', text: 'text-red-400', glow: 'shadow-red-500/30' };
  };

  const colors = getColor();
  const circumference = 2 * Math.PI * 18;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center">
      <svg className="w-14 h-14 transform -rotate-90">
        {/* Background circle */}
        <circle
          cx="28"
          cy="28"
          r="18"
          stroke="currentColor"
          strokeWidth="3"
          fill="none"
          className="text-dark-700"
        />
        {/* Progress circle */}
        <motion.circle
          cx="28"
          cy="28"
          r="18"
          stroke="currentColor"
          strokeWidth="3"
          fill="none"
          strokeLinecap="round"
          className={colors.text}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1, ease: 'easeOut' }}
          style={{
            strokeDasharray: circumference,
          }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className={`text-sm font-bold ${colors.text}`}
        >
          {score}%
        </motion.span>
      </div>
    </div>
  );
};

export default MatchScore;


