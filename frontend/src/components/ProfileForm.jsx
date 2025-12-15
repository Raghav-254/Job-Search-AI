import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Briefcase, Building2, Clock, Code, DollarSign, MapPin, ChevronDown, ChevronUp } from 'lucide-react';
import { getAvailableCompanies } from '../services/api';
import ChipInput from './ChipInput';
import Autocomplete from './Autocomplete';
import { SKILL_SUGGESTIONS, LOCATION_SUGGESTIONS, COMPANY_SUGGESTIONS } from '../data/suggestions';

const ProfileForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    role: '',
    company: '',
    years_of_experience: '',
    skills: [],
    expected_salary: '',
    location: '',
    target_companies: [],
  });
  
  const [availableCompanies, setAvailableCompanies] = useState({ greenhouse: [], lever: [] });
  const [showCompanySelector, setShowCompanySelector] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const companies = await getAvailableCompanies();
        setAvailableCompanies(companies);
      } catch (error) {
        console.error('Failed to fetch companies:', error);
      }
    };
    fetchCompanies();
  }, []);

  const allCompanies = [...availableCompanies.greenhouse, ...availableCompanies.lever].sort();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleCompanyToggle = (company) => {
    setFormData(prev => {
      const isSelected = prev.target_companies.includes(company);
      return {
        ...prev,
        target_companies: isSelected
          ? prev.target_companies.filter(c => c !== company)
          : [...prev.target_companies, company]
      };
    });
  };

  const selectAllCompanies = () => {
    setFormData(prev => ({ ...prev, target_companies: [...allCompanies] }));
  };

  const clearAllCompanies = () => {
    setFormData(prev => ({ ...prev, target_companies: [] }));
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.role.trim()) newErrors.role = 'Role is required';
    if (!formData.company.trim()) newErrors.company = 'Company is required';
    if (!formData.years_of_experience) newErrors.years_of_experience = 'Experience is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    const submitData = {
      role: formData.role,
      company: formData.company,
      years_of_experience: parseInt(formData.years_of_experience),
      skills: formData.skills.length > 0 ? formData.skills : null,
      expected_salary: formData.expected_salary ? parseInt(formData.expected_salary) : null,
      location: formData.location || null,
      target_companies: formData.target_companies.length > 0 ? formData.target_companies : null,
    };

    onSubmit(submitData);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-2xl mx-auto"
    >
      <div className="glass rounded-2xl p-8 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="font-display text-4xl font-bold gradient-text mb-2">
            Find Your Next Role
          </h1>
          <p className="text-dark-400">
            Tell us about yourself and we'll find the best matching jobs
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Required Fields */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-dark-300 mb-2">
                <Briefcase size={16} />
                Current Role *
              </label>
              <input
                type="text"
                name="role"
                value={formData.role}
                onChange={handleChange}
                placeholder="e.g., Frontend Engineer"
                className={`w-full px-4 py-3 rounded-xl bg-dark-800 border ${
                  errors.role ? 'border-red-500' : 'border-dark-600'
                } focus:border-brand-500 transition-colors`}
              />
              {errors.role && <p className="text-red-400 text-sm mt-1">{errors.role}</p>}
            </div>

            <div>
              <Autocomplete
                value={formData.company}
                onChange={(value) => setFormData(prev => ({ ...prev, company: value }))}
                suggestions={COMPANY_SUGGESTIONS}
                placeholder="e.g., Google"
                label="Current Company *"
                icon={Building2}
              />
              {errors.company && <p className="text-red-400 text-sm mt-1">{errors.company}</p>}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-dark-300 mb-2">
                <Clock size={16} />
                Years of Experience *
              </label>
              <input
                type="number"
                name="years_of_experience"
                value={formData.years_of_experience}
                onChange={handleChange}
                min="0"
                max="50"
                placeholder="e.g., 5"
                className={`w-full px-4 py-3 rounded-xl bg-dark-800 border ${
                  errors.years_of_experience ? 'border-red-500' : 'border-dark-600'
                } focus:border-brand-500 transition-colors`}
              />
              {errors.years_of_experience && (
                <p className="text-red-400 text-sm mt-1">{errors.years_of_experience}</p>
              )}
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-dark-300 mb-2">
                <DollarSign size={16} />
                Expected Salary (USD)
              </label>
              <input
                type="number"
                name="expected_salary"
                value={formData.expected_salary}
                onChange={handleChange}
                placeholder="e.g., 200000"
                className="w-full px-4 py-3 rounded-xl bg-dark-800 border border-dark-600 focus:border-brand-500 transition-colors"
              />
            </div>
          </div>

          {/* Skills with Chip Input */}
          <ChipInput
            value={formData.skills}
            onChange={(skills) => setFormData(prev => ({ ...prev, skills }))}
            suggestions={SKILL_SUGGESTIONS}
            placeholder="Type a skill and press Enter..."
            label="Skills"
            icon={Code}
            maxItems={15}
          />

          {/* Location with Autocomplete */}
          <Autocomplete
            value={formData.location}
            onChange={(value) => setFormData(prev => ({ ...prev, location: value }))}
            suggestions={LOCATION_SUGGESTIONS}
            placeholder="e.g., San Francisco, Remote"
            label="Preferred Location"
            icon={MapPin}
          />

          {/* Target Companies Selector */}
          <div className="border-t border-dark-600 pt-6">
            <button
              type="button"
              onClick={() => setShowCompanySelector(!showCompanySelector)}
              className="flex items-center justify-between w-full text-left"
            >
              <div className="flex items-center gap-2">
                <Building2 size={16} className="text-dark-400" />
                <span className="text-sm font-medium text-dark-300">
                  Target Companies to Search
                  {formData.target_companies.length > 0 && (
                    <span className="ml-2 text-brand-400">
                      ({formData.target_companies.length} selected)
                    </span>
                  )}
                </span>
              </div>
              {showCompanySelector ? (
                <ChevronUp size={16} className="text-dark-400" />
              ) : (
                <ChevronDown size={16} className="text-dark-400" />
              )}
            </button>
            <p className="text-xs text-dark-500 mt-1">
              Leave empty to search all available companies
            </p>

            {showCompanySelector && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-4"
              >
                <div className="flex gap-2 mb-3">
                  <button
                    type="button"
                    onClick={selectAllCompanies}
                    className="text-xs text-brand-400 hover:text-brand-300 transition-colors"
                  >
                    Select All
                  </button>
                  <span className="text-dark-600">|</span>
                  <button
                    type="button"
                    onClick={clearAllCompanies}
                    className="text-xs text-dark-400 hover:text-dark-300 transition-colors"
                  >
                    Clear All
                  </button>
                </div>
                
                {/* Company sources */}
                <div className="space-y-4">
                  {/* Greenhouse companies */}
                  <div>
                    <p className="text-xs text-dark-500 mb-2 flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                      Greenhouse ({availableCompanies.greenhouse.length} companies)
                    </p>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2 p-3 bg-dark-900 rounded-xl">
                      {availableCompanies.greenhouse.map(company => (
                        <label
                          key={company}
                          className="flex items-center gap-2 cursor-pointer hover:bg-dark-800 p-2 rounded-lg transition-colors"
                        >
                          <input
                            type="checkbox"
                            checked={formData.target_companies.includes(company)}
                            onChange={() => handleCompanyToggle(company)}
                            className="rounded"
                          />
                          <span className="text-sm text-dark-200 capitalize">
                            {company.replace(/-/g, ' ')}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Lever companies */}
                  <div>
                    <p className="text-xs text-dark-500 mb-2 flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                      Lever ({availableCompanies.lever.length} companies)
                    </p>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2 p-3 bg-dark-900 rounded-xl">
                      {availableCompanies.lever.map(company => (
                        <label
                          key={company}
                          className="flex items-center gap-2 cursor-pointer hover:bg-dark-800 p-2 rounded-lg transition-colors"
                        >
                          <input
                            type="checkbox"
                            checked={formData.target_companies.includes(company)}
                            onChange={() => handleCompanyToggle(company)}
                            className="rounded"
                          />
                          <span className="text-sm text-dark-200 capitalize">
                            {company.replace(/-/g, ' ')}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </div>

          {/* Submit Button */}
          <motion.button
            type="submit"
            disabled={isLoading}
            whileHover={{ scale: isLoading ? 1 : 1.02 }}
            whileTap={{ scale: isLoading ? 1 : 0.98 }}
            className={`w-full py-4 rounded-xl font-semibold text-lg flex items-center justify-center gap-2 transition-all ${
              isLoading
                ? 'bg-dark-600 cursor-not-allowed'
                : 'bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 shadow-lg shadow-brand-500/25'
            }`}
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                Analyzing...
              </>
            ) : (
              <>
                <Search size={20} />
                Find Jobs
              </>
            )}
          </motion.button>
        </form>
      </div>
    </motion.div>
  );
};

export default ProfileForm;
