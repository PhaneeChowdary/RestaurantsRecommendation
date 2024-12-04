import React, { useState, useEffect } from 'react';
import { Filter, ChevronDown } from 'lucide-react';

const AdvancedFilters = ({ onFilterChange, currentFilters = {} }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filterOptions, setFilterOptions] = useState(null);

  // Add star rating options
  const starOptions = [
    { value: "5", label: "5 Stars" },
    { value: "4", label: "4+ Stars" },
    { value: "3", label: "3+ Stars" },
    { value: "2", label: "2+ Stars" }
  ];

  // Define all filter options
  const wifiOptions = [
    { value: "free", label: "Free WiFi" },
    { value: "paid", label: "Paid WiFi" },
    { value: "no", label: "No WiFi" }
  ];

  const alcoholOptions = [
    { value: "none", label: "No Alcohol" },
    { value: "beer_and_wine", label: "Beer and Wine" },
    { value: "full_bar", label: "Full Bar" }
  ];

  useEffect(() => {
    fetchFilterOptions();
  }, []);

  const fetchFilterOptions = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/filters');
      const data = await response.json();
      console.log('Fetched filter options:', data);  // Debug log
      setFilterOptions(data);
    } catch (error) {
      console.error('Failed to fetch filter options:', error);
    }
  };

  const handleFilterChange = (type, value) => {
    console.log(`Changing filter ${type} to:`, value);  // Debug log
    const newFilters = {
      ...currentFilters,
      [type]: value
    };
    console.log('New filters being sent:', newFilters);  // Debug log
    onFilterChange(newFilters);
  };

  const handleParkingChange = (type) => {
    const currentParking = currentFilters.parking || {};
    const newParking = {
      ...currentParking,
      [type]: !currentParking[type]
    };
    console.log('New parking configuration:', newParking);  // Debug log
    handleFilterChange('parking', newParking);
  };

  // Count active filters
  const getActiveFilterCount = () => {
    let count = 0;
    Object.entries(currentFilters).forEach(([key, value]) => {
      if (value && value !== '' && key !== 'city' && key !== 'price_range_min') {
        if (key === 'parking' && typeof value === 'object') {
          count += Object.values(value).filter(Boolean).length;
        } else {
          count += 1;
        }
      }
    });
    return count;
  };

  if (!filterOptions) return null;

  return (
    <div className="relative mb-4">
      <div className="flex items-center gap-2">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg shadow-sm hover:bg-gray-50"
        >
          <Filter size={20} />
          Advanced Filters
          <ChevronDown 
            size={16} 
            className={`transform transition-transform ${isOpen ? 'rotate-180' : ''}`}
          />
        </button>

        {getActiveFilterCount() > 0 && (
          <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
            {getActiveFilterCount()} active
          </span>
        )}
      </div>

      {isOpen && (
        <div className="absolute z-10 mt-2 w-96 bg-white border rounded-lg shadow-lg p-4">
          {/* WiFi */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">WiFi</label>
            <select
              value={currentFilters.wifi || ''}
              onChange={(e) => {
                console.log('Selected WiFi value:', e.target.value);
                handleFilterChange('wifi', e.target.value);
              }}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Any</option>
              {wifiOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Delivery */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Delivery</label>
            <select
              value={currentFilters.delivery || ''}
              onChange={(e) => handleFilterChange('delivery', e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Any</option>
              <option value="true">Available</option>
              <option value="false">Not Available</option>
            </select>
          </div>

          {/* Star Rating Filter */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Star Rating</label>
            <select
              value={currentFilters.minStars || ''}
              onChange={(e) => handleFilterChange('minStars', e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Any Rating</option>
              {starOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          
          {/* Alcohol */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Alcohol</label>
            <select
              value={currentFilters.alcohol || ''}
              onChange={(e) => handleFilterChange('alcohol', e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Any</option>
              {alcoholOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Pets Allowed */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Pets Allowed</label>
            <select
              value={currentFilters.pets_allowed || ''}
              onChange={(e) => handleFilterChange('pets_allowed', e.target.value)}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">Any</option>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          </div>

          {/* Smoking */}
          <div className="mb-4">
              <label className="block text-sm font-medium mb-1">Smoking</label>
              <select
                value={currentFilters.smoking || ''}
                onChange={(e) => handleFilterChange('smoking', e.target.value)}
                className="w-full px-3 py-2 border rounded"
              >
                <option value="">Any</option>
                {filterOptions.smoking?.map(option => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>

          {/* Parking Options */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Parking Options</label>
            <div className="space-y-2">
              {Object.entries(filterOptions.parking || {}).map(([type, _]) => (
                <label key={type} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={currentFilters.parking?.[type] || false}
                    onChange={() => handleParkingChange(type)}
                    className="mr-2 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-sm">{type.charAt(0).toUpperCase() + type.slice(1)}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedFilters;