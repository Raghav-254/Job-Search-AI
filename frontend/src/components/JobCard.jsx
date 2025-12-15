import { motion } from 'framer-motion';
import { MapPin, ExternalLink, Building2, Sparkles } from 'lucide-react';
import MatchScore from './MatchScore';

const JobCard = ({ job, index }) => {
  const { title, company, location, url, match_score, insight, match_reasons, source } = job;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      className="glass rounded-xl p-6 hover:border-brand-500/50 transition-all duration-300 group"
    >
      <div className="flex gap-4">
        {/* Match Score */}
        <div className="flex-shrink-0">
          <MatchScore score={match_score} />
        </div>

        {/* Job Info */}
        <div className="flex-grow min-w-0">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <h3 className="font-semibold text-lg text-white truncate group-hover:text-brand-300 transition-colors">
                {title}
              </h3>
              <div className="flex items-center gap-2 mt-1">
                <Building2 size={14} className="text-dark-400 flex-shrink-0" />
                <span className="text-dark-300 capitalize">{company}</span>
                <span className="text-dark-600">•</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-dark-700 text-dark-300 capitalize">
                  {source}
                </span>
              </div>
              {location && (
                <div className="flex items-center gap-2 mt-1">
                  <MapPin size={14} className="text-dark-400 flex-shrink-0" />
                  <span className="text-dark-400 text-sm">{location}</span>
                </div>
              )}
            </div>

            {/* Apply Button */}
            <motion.a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex-shrink-0 px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm flex items-center gap-2 transition-colors shadow-lg shadow-brand-500/20"
            >
              Apply
              <ExternalLink size={14} />
            </motion.a>
          </div>

          {/* AI Insight */}
          <div className="mt-4 p-3 rounded-lg bg-dark-800/50 border border-dark-700">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles size={14} className="text-brand-400" />
              <span className="text-xs font-medium text-brand-400">AI Insight</span>
            </div>
            <p className="text-sm text-dark-300">{insight}</p>
          </div>

          {/* Match Reasons */}
          {match_reasons && match_reasons.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {match_reasons.map((reason, idx) => (
                <span
                  key={idx}
                  className="text-xs px-2 py-1 rounded-full bg-dark-800 text-dark-300 border border-dark-700"
                >
                  {reason}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default JobCard;


