import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Building2, ChevronDown, ChevronUp, Sparkles, X } from 'lucide-react';
import JobCard from './JobCard';

const JobResults = ({ data, onBack }) => {
  const { profile, jobs, total_jobs, companies_searched } = data;
  const [showProfileDetails, setShowProfileDetails] = useState(false);
  const [showCompaniesModal, setShowCompaniesModal] = useState(false);

  // Get top companies to display (first 5)
  const topCompanies = companies_searched.slice(0, 5);
  const remainingCount = companies_searched.length - topCompanies.length;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="w-full max-w-4xl mx-auto"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-dark-400 hover:text-white transition-colors"
        >
          <ArrowLeft size={18} />
          <span className="text-sm">New Search</span>
        </button>
        <div className="text-sm font-medium text-brand-400">
          {total_jobs} jobs found
        </div>
      </div>

      {/* Companies Searched Bar - Trust Indicator */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center gap-2 mb-4 p-3 rounded-xl bg-dark-800/50 border border-dark-700"
      >
        <Building2 size={16} className="text-dark-400 flex-shrink-0" />
        <span className="text-xs text-dark-400 flex-shrink-0">Searched:</span>
        <div className="flex items-center gap-2 flex-wrap flex-1 min-w-0">
          {topCompanies.map((company, idx) => (
            <span
              key={idx}
              className="text-xs px-2 py-1 rounded-md bg-dark-700 text-dark-200 capitalize whitespace-nowrap"
            >
              {company.replace(/-/g, ' ')}
            </span>
          ))}
          {remainingCount > 0 && (
            <button
              onClick={() => setShowCompaniesModal(true)}
              className="text-xs px-2 py-1 rounded-md bg-brand-500/20 text-brand-400 hover:bg-brand-500/30 transition-colors whitespace-nowrap"
            >
              +{remainingCount} more
            </button>
          )}
        </div>
      </motion.div>

      {/* Companies Modal */}
      <AnimatePresence>
        {showCompaniesModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
            onClick={() => setShowCompaniesModal(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="glass rounded-2xl p-6 max-w-lg w-full max-h-[70vh] overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-lg flex items-center gap-2">
                  <Building2 size={20} className="text-brand-400" />
                  {companies_searched.length} Companies Searched
                </h3>
                <button
                  onClick={() => setShowCompaniesModal(false)}
                  className="text-dark-400 hover:text-white transition-colors"
                >
                  <X size={20} />
                </button>
              </div>
              <div className="overflow-y-auto max-h-[50vh] pr-2">
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {companies_searched.map((company, idx) => (
                    <span
                      key={idx}
                      className="text-sm px-3 py-2 rounded-lg bg-dark-800 text-dark-200 capitalize text-center"
                    >
                      {company.replace(/-/g, ' ')}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Compact Profile Summary Bar */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass rounded-xl p-3 mb-4"
      >
        <button
          onClick={() => setShowProfileDetails(!showProfileDetails)}
          className="w-full flex items-center justify-between"
        >
          <div className="flex items-center gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <Sparkles size={16} className="text-brand-400" />
              <span className="text-sm font-medium">{profile.original_role}</span>
            </div>
            <span className="text-dark-600 hidden sm:inline">•</span>
            <span className="text-sm text-dark-400">{profile.seniority_level}</span>
            <span className="text-dark-600 hidden sm:inline">•</span>
            <span className="text-sm text-dark-400">{profile.expected_salary_range}</span>
          </div>
          <div className="flex items-center gap-2 text-dark-400">
            <span className="text-xs hidden sm:inline">
              {showProfileDetails ? 'Hide' : 'Details'}
            </span>
            {showProfileDetails ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </button>

        {/* Expandable Profile Details */}
        <AnimatePresence>
          {showProfileDetails && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="overflow-hidden"
            >
              <div className="pt-4 mt-3 border-t border-dark-700">
                {/* Stats Row */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                  <div className="p-2 rounded-lg bg-dark-800/50">
                    <p className="text-xs text-dark-500">Role</p>
                    <p className="text-sm font-medium truncate">{profile.original_role}</p>
                  </div>
                  <div className="p-2 rounded-lg bg-dark-800/50">
                    <p className="text-xs text-dark-500">Company Tier</p>
                    <p className="text-sm font-medium">{profile.company_tier}</p>
                  </div>
                  <div className="p-2 rounded-lg bg-dark-800/50">
                    <p className="text-xs text-dark-500">Seniority</p>
                    <p className="text-sm font-medium">{profile.seniority_level}</p>
                  </div>
                  <div className="p-2 rounded-lg bg-dark-800/50">
                    <p className="text-xs text-dark-500">Salary Range</p>
                    <p className="text-sm font-medium">{profile.expected_salary_range}</p>
                  </div>
                </div>

                {/* Skills - Compact */}
                <div className="mb-3">
                  <p className="text-xs text-dark-500 mb-1">Inferred Skills</p>
                  <div className="flex flex-wrap gap-1">
                    {profile.inferred_skills.slice(0, 8).map((skill, idx) => (
                      <span
                        key={idx}
                        className="text-xs px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400"
                      >
                        {skill}
                      </span>
                    ))}
                    {profile.inferred_skills.length > 8 && (
                      <span className="text-xs px-2 py-0.5 text-dark-500">
                        +{profile.inferred_skills.length - 8} more
                      </span>
                    )}
                  </div>
                </div>

                {/* Target Titles - Compact */}
                <div>
                  <p className="text-xs text-dark-500 mb-1">Searching for</p>
                  <div className="flex flex-wrap gap-1">
                    {profile.target_titles.slice(0, 6).map((title, idx) => (
                      <span
                        key={idx}
                        className="text-xs px-2 py-0.5 rounded-full bg-dark-700 text-dark-300"
                      >
                        {title}
                      </span>
                    ))}
                    {profile.target_titles.length > 6 && (
                      <span className="text-xs px-2 py-0.5 text-dark-500">
                        +{profile.target_titles.length - 6} more
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Job List */}
      {jobs.length > 0 ? (
        <div className="space-y-4">
          {jobs.map((job, index) => (
            <JobCard key={job.id} job={job} index={index} />
          ))}
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass rounded-2xl p-12 text-center"
        >
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-xl font-semibold mb-2">No Matching Jobs Found</h3>
          <p className="text-dark-400">
            Try adjusting your search criteria or selecting different companies.
          </p>
        </motion.div>
      )}
    </motion.div>
  );
};

export default JobResults;
