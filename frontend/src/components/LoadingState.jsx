import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Search, Brain, ListChecks, Building2, CheckCircle2, Loader2 } from 'lucide-react';

const steps = [
  { icon: Brain, text: 'Analyzing your profile', subtext: 'Understanding your skills & experience' },
  { icon: Building2, text: 'Scanning companies', subtext: 'Checking 150+ top companies' },
  { icon: Search, text: 'Fetching job listings', subtext: 'Greenhouse, Lever & more' },
  { icon: Sparkles, text: 'AI ranking matches', subtext: 'Finding the best fit for you' },
  { icon: ListChecks, text: 'Preparing results', subtext: 'Sorting by relevance & location' },
];

const tips = [
  "💡 Tip: Remote-friendly companies often have flexible interview processes",
  "🎯 Did you know? We prioritize jobs matching your exact experience level",
  "🌍 Fun fact: We search across India, Europe, and US job markets",
  "⚡ Pro tip: Jobs from your preferred location appear first",
  "🏢 We check both Greenhouse and Lever career pages",
  "🤖 Our AI evaluates each job against your specific skills",
];

const companyNames = [
  'Google', 'Meta', 'Amazon', 'Microsoft', 'Razorpay', 'Flipkart',
  'Swiggy', 'Atlassian', 'Stripe', 'Databricks', 'Notion', 'Figma'
];

const LoadingState = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [tipIndex, setTipIndex] = useState(0);
  const [visibleCompanies, setVisibleCompanies] = useState([]);

  // Cycle through steps
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // Cycle through tips
  useEffect(() => {
    const interval = setInterval(() => {
      setTipIndex((prev) => (prev + 1) % tips.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  // Animate companies appearing
  useEffect(() => {
    const shuffled = [...companyNames].sort(() => Math.random() - 0.5);
    let index = 0;
    const interval = setInterval(() => {
      if (index < shuffled.length) {
        setVisibleCompanies((prev) => [...prev.slice(-5), shuffled[index]]);
        index++;
      } else {
        index = 0;
        setVisibleCompanies([]);
      }
    }, 800);
    return () => clearInterval(interval);
  }, []);

  const progress = ((activeStep + 1) / steps.length) * 100;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-lg mx-auto py-8"
    >
      <div className="glass rounded-2xl p-8 relative overflow-hidden">
        {/* Background gradient animation */}
        <div className="absolute inset-0 opacity-30">
          <motion.div
            animate={{
              background: [
                'radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 50%)',
                'radial-gradient(circle at 80% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 50%)',
                'radial-gradient(circle at 50% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%)',
                'radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 50%)',
              ],
            }}
            transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
            className="absolute inset-0"
          />
        </div>

        <div className="relative z-10">
          {/* Header */}
          <div className="text-center mb-8">
            <motion.div
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-brand-500/20 mb-4"
            >
              <Sparkles className="text-brand-400" size={28} />
            </motion.div>
            <h2 className="text-xl font-semibold mb-1">Finding Your Perfect Match</h2>
            <p className="text-sm text-dark-400">This usually takes 15-30 seconds</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="h-1.5 bg-dark-700 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5, ease: 'easeOut' }}
                className="h-full bg-gradient-to-r from-brand-500 to-brand-400 rounded-full"
              />
            </div>
            <div className="flex justify-between mt-2">
              <span className="text-xs text-dark-500">Step {activeStep + 1} of {steps.length}</span>
              <span className="text-xs text-brand-400">{Math.round(progress)}%</span>
            </div>
          </div>

          {/* Steps */}
          <div className="space-y-3 mb-8">
            {steps.map((step, index) => {
              const isActive = index === activeStep;
              const isComplete = index < activeStep;
              const isPending = index > activeStep;

              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 ${
                    isActive
                      ? 'bg-brand-500/10 border border-brand-500/30'
                      : isComplete
                      ? 'bg-dark-800/30'
                      : 'opacity-40'
                  }`}
                >
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    isComplete
                      ? 'bg-green-500/20'
                      : isActive
                      ? 'bg-brand-500/20'
                      : 'bg-dark-700'
                  }`}>
                    {isComplete ? (
                      <CheckCircle2 size={16} className="text-green-400" />
                    ) : isActive ? (
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
                      >
                        <Loader2 size={16} className="text-brand-400" />
                      </motion.div>
                    ) : (
                      <step.icon size={16} className="text-dark-500" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm font-medium ${
                      isComplete ? 'text-dark-300' : isActive ? 'text-white' : 'text-dark-500'
                    }`}>
                      {step.text}
                    </p>
                    <p className={`text-xs ${
                      isActive ? 'text-dark-400' : 'text-dark-600'
                    }`}>
                      {step.subtext}
                    </p>
                  </div>
                  {isComplete && (
                    <span className="text-xs text-green-400">Done</span>
                  )}
                </motion.div>
              );
            })}
          </div>

          {/* Animated Companies Being Searched */}
          <div className="mb-6">
            <p className="text-xs text-dark-500 mb-2 text-center">Currently checking...</p>
            <div className="flex justify-center gap-2 h-8 overflow-hidden">
              <AnimatePresence mode="popLayout">
                {visibleCompanies.map((company, index) => (
                  <motion.span
                    key={`${company}-${index}`}
                    initial={{ opacity: 0, scale: 0.8, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.8, y: -20 }}
                    className="text-xs px-3 py-1.5 rounded-full bg-dark-700 text-dark-300 whitespace-nowrap"
                  >
                    {company}
                  </motion.span>
                ))}
              </AnimatePresence>
            </div>
          </div>

          {/* Rotating Tips */}
          <div className="border-t border-dark-700 pt-4">
            <AnimatePresence mode="wait">
              <motion.p
                key={tipIndex}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className="text-xs text-dark-400 text-center"
              >
                {tips[tipIndex]}
              </motion.p>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default LoadingState;
