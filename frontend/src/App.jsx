import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import ProfileForm from './components/ProfileForm';
import JobResults from './components/JobResults';
import LoadingState from './components/LoadingState';
import { analyzeProfile } from './services/api';
import { Sparkles, Github } from 'lucide-react';

function App() {
  const [view, setView] = useState('form'); // 'form', 'loading', 'results'
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (profileData) => {
    setView('loading');
    setError(null);

    try {
      const data = await analyzeProfile(profileData);
      setResults(data);
      setView('results');
    } catch (err) {
      console.error('Error analyzing profile:', err);
      setError(err.response?.data?.detail || 'Failed to analyze profile. Please try again.');
      setView('form');
    }
  };

  const handleBack = () => {
    setView('form');
    setResults(null);
  };

  return (
    <div className="min-h-screen py-8 px-4">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-brand-600/10 rounded-full blur-3xl" />
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center gap-2 mb-2">
            <Sparkles className="text-brand-400" size={28} />
            <span className="font-display text-2xl font-bold gradient-text">
              JobMatch AI
            </span>
          </div>
          <p className="text-dark-400 text-sm">
            AI-powered job search assistant
          </p>
        </motion.header>

        {/* Error Alert */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="max-w-2xl mx-auto mb-6"
            >
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-center">
                {error}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Main Content */}
        <AnimatePresence mode="wait">
          {view === 'form' && (
            <motion.div
              key="form"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <ProfileForm onSubmit={handleSubmit} isLoading={false} />
            </motion.div>
          )}

          {view === 'loading' && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <LoadingState />
            </motion.div>
          )}

          {view === 'results' && results && (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <JobResults data={results} onBack={handleBack} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-center mt-12 text-dark-500 text-sm"
        >
          <p>
            Powered by AI • Jobs from Greenhouse & Lever
          </p>
        </motion.footer>
      </div>
    </div>
  );
}

export default App;


