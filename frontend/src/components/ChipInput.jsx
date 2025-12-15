import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

const ChipInput = ({ 
  value = [], 
  onChange, 
  suggestions = [], 
  placeholder = 'Type to search...',
  label,
  icon: Icon,
  maxItems = 10,
}) => {
  const [inputValue, setInputValue] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const inputRef = useRef(null);
  const containerRef = useRef(null);

  // Filter suggestions based on input
  const filteredSuggestions = suggestions.filter(
    (suggestion) =>
      suggestion.toLowerCase().includes(inputValue.toLowerCase()) &&
      !value.includes(suggestion)
  ).slice(0, 8);

  // Handle click outside to close suggestions
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const addChip = (chip) => {
    if (chip && !value.includes(chip) && value.length < maxItems) {
      onChange([...value, chip]);
      setInputValue('');
      setShowSuggestions(false);
      setHighlightedIndex(0);
    }
  };

  const removeChip = (chipToRemove) => {
    onChange(value.filter((chip) => chip !== chipToRemove));
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredSuggestions.length > 0 && showSuggestions) {
        addChip(filteredSuggestions[highlightedIndex]);
      } else if (inputValue.trim()) {
        addChip(inputValue.trim());
      }
    } else if (e.key === 'Backspace' && !inputValue && value.length > 0) {
      removeChip(value[value.length - 1]);
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlightedIndex((prev) =>
        prev < filteredSuggestions.length - 1 ? prev + 1 : prev
      );
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : 0));
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  return (
    <div ref={containerRef} className="relative">
      {label && (
        <label className="flex items-center gap-2 text-sm font-medium text-dark-300 mb-2">
          {Icon && <Icon size={16} />}
          {label}
        </label>
      )}
      
      <div
        className="min-h-[48px] px-3 py-2 rounded-xl bg-dark-800 border border-dark-600 focus-within:border-brand-500 transition-colors flex flex-wrap gap-2 cursor-text"
        onClick={() => inputRef.current?.focus()}
      >
        <AnimatePresence>
          {value.map((chip) => (
            <motion.span
              key={chip}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-brand-500/20 text-brand-300 text-sm border border-brand-500/30"
            >
              {chip}
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  removeChip(chip);
                }}
                className="hover:text-brand-100 transition-colors"
              >
                <X size={14} />
              </button>
            </motion.span>
          ))}
        </AnimatePresence>
        
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            setShowSuggestions(true);
            setHighlightedIndex(0);
          }}
          onFocus={() => setShowSuggestions(true)}
          onKeyDown={handleKeyDown}
          placeholder={value.length === 0 ? placeholder : ''}
          className="flex-1 min-w-[120px] bg-transparent outline-none text-white placeholder-dark-500"
          disabled={value.length >= maxItems}
        />
      </div>

      {/* Suggestions Dropdown */}
      <AnimatePresence>
        {showSuggestions && filteredSuggestions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute z-50 w-full mt-2 py-2 rounded-xl bg-dark-800 border border-dark-600 shadow-xl max-h-48 overflow-y-auto"
          >
            {filteredSuggestions.map((suggestion, index) => (
              <button
                key={suggestion}
                type="button"
                onClick={() => addChip(suggestion)}
                className={`w-full px-4 py-2 text-left text-sm transition-colors ${
                  index === highlightedIndex
                    ? 'bg-brand-500/20 text-brand-300'
                    : 'text-dark-200 hover:bg-dark-700'
                }`}
              >
                {suggestion}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {value.length >= maxItems && (
        <p className="text-xs text-dark-500 mt-1">
          Maximum {maxItems} items reached
        </p>
      )}
    </div>
  );
};

export default ChipInput;

