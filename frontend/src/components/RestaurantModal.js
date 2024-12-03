import React, { useState, useEffect } from 'react';
import { createRestaurant, updateRestaurant } from '../utils/api';

const RestaurantModal = ({ isOpen, onClose, restaurant, mode = 'create' }) => {
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    city: '',
    state: '',
    categories: '',
    price_range: '1',
    wifi: 'no',
    parking: {
      garage: false,
      street: false,
      lot: false,
      valet: false
    }
  });

  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (restaurant && mode === 'edit') {
      // Parse the BusinessParking string into an object
      let parkingObj = { garage: false, street: false, lot: false, valet: false };
      if (restaurant.attributes?.BusinessParking) {
        try {
          parkingObj = JSON.parse(
            restaurant.attributes.BusinessParking.replace(/'/g, '"')
          );
        } catch (e) {
          console.error('Error parsing parking data:', e);
        }
      }

      setFormData({
        name: restaurant.name || '',
        address: restaurant.address || '',
        city: restaurant.city || '',
        state: restaurant.state || '',
        categories: restaurant.categories || '',
        price_range: restaurant.attributes?.RestaurantsPriceRange2 || '1',
        wifi: restaurant.attributes?.WiFi || 'no',
        parking: parkingObj
      });
    }
  }, [restaurant, mode]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleParkingChange = (type) => {
    setFormData(prev => ({
      ...prev,
      parking: {
        ...prev.parking,
        [type]: !prev.parking[type]
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      if (mode === 'create') {
        await createRestaurant(formData);
      } else {
        await updateRestaurant(restaurant._id.$oid, formData);
      }
      onClose(true); // Refresh the restaurant list
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">
          {mode === 'create' ? 'Add New Restaurant' : 'Edit Restaurant'}
        </h2>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Restaurant Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Address</label>
            <input
              type="text"
              name="address"
              value={formData.address}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">City</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">State</label>
              <input
                type="text"
                name="state"
                value={formData.state}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded"
                required
                maxLength={2}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Categories</label>
            <input
              type="text"
              name="categories"
              value={formData.categories}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded"
              placeholder="e.g., Italian, Pizza, Restaurants"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Price Range</label>
            <select
              name="price_range"
              value={formData.price_range}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="1">$ (Inexpensive)</option>
              <option value="2">$$ (Moderate)</option>
              <option value="3">$$$ (Expensive)</option>
              <option value="4">$$$$ (Very Expensive)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">WiFi</label>
            <select
              name="wifi"
              value={formData.wifi}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="no">No WiFi</option>
              <option value="free">Free WiFi</option>
              <option value="paid">Paid WiFi</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Parking Options</label>
            <div className="space-y-2">
              {Object.entries(formData.parking).map(([type, value]) => (
                <label key={type} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={value}
                    onChange={() => handleParkingChange(type)}
                    className="mr-2"
                  />
                  <span className="text-sm">
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </span>
                </label>
              ))}
            </div>
          </div>

          <div className="flex justify-end space-x-4 mt-6">
            <button
              type="button"
              onClick={() => onClose(false)}
              className="px-4 py-2 border rounded hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {isSubmitting ? 'Saving...' : mode === 'create' ? 'Create' : 'Update'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RestaurantModal;