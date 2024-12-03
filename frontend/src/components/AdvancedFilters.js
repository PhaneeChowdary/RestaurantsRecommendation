import React, { useState, useEffect } from 'react';
import { Filter, ChevronDown } from 'lucide-react';
import { fetchCategories } from '../utils/api';

const AdvancedFilters = ({ onFilterChange }) => {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [sortBy, setSortBy] = useState('stars');
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const data = await fetchCategories();
      setCategories(data);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const handleFilterChange = (type, value) => {
    if (type === 'category') {
      setSelectedCategory(value);
    } else if (type === 'sort') {
      setSortBy(value);
    }
    
    onFilterChange({
      category: type === 'category' ? value : selectedCategory,
      sort: type === 'sort' ? value : sortBy
    });
  };

  return (
    <div className="relative mb-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg shadow-sm"
      >
        <Filter size={20} />
        Advanced Filters
        <ChevronDown size={16} className={`transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute z-10 mt-2 w-64 bg-white border rounded-lg shadow-lg p-4">
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => handleFilterChange('category', e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">All Categories</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => handleFilterChange('sort', e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="stars">Rating (High to Low)</option>
              <option value="-stars">Rating (Low to High)</option>
              <option value="review_count">Most Reviewed</option>
              <option value="name">Name (A-Z)</option>
              <option value="-name">Name (Z-A)</option>
            </select>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedFilters;