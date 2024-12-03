import React, { useState, useEffect, useCallback } from 'react';
import { Search, Plus, Edit2, Trash2, Star } from 'lucide-react';
import { fetchRestaurants, deleteRestaurant } from '../utils/api';
import RestaurantModal from './RestaurantModal';
import ErrorToast from './ErrorToast';
import LoadingSpinner from './LoadingSpinner';
import AdvancedFilters from './AdvancedFilters';

const RestaurantApp = () => {
  // Basic state
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  // Filter states
  const [city, setCity] = useState('');
  const [priceRange, setPriceRange] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [sortBy, setSortBy] = useState('stars');
  const [sortOrder, setSortOrder] = useState('-1');
  
  // Modal states
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [modalMode, setModalMode] = useState('create');
  
  // Delete dialog states
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [restaurantToDelete, setRestaurantToDelete] = useState(null);

  useEffect(() => {
    loadRestaurants();
  }, [city, priceRange, selectedCategory, sortBy, sortOrder, page]);

  const loadRestaurants = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetchRestaurants({
        city,
        price_range_min: priceRange,
        categories: selectedCategory,
        page,
        per_page: 10,
        sort: sortBy,
        order: sortOrder
      });
      setRestaurants(data.restaurants);
      setTotalPages(data.total_pages);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [city, priceRange, selectedCategory, sortBy, sortOrder, page]);

  useEffect(() => {
    loadRestaurants();
  }, [loadRestaurants]); 

  const handleAdvancedFilters = ({ category, sort }) => {
    setSelectedCategory(category);
    if (sort) {
      if (sort.startsWith('-')) {
        setSortBy(sort.substring(1));
        setSortOrder('1');
      } else {
        setSortBy(sort);
        setSortOrder('-1');
      }
    }
    setPage(1);
  };

  const handleAddNew = () => {
    setSelectedRestaurant(null);
    setModalMode('create');
    setModalOpen(true);
  };

  const handleEdit = (restaurant) => {
    setSelectedRestaurant(restaurant);
    setModalMode('edit');
    setModalOpen(true);
  };

  const handleDelete = async () => {
    if (!restaurantToDelete) return;

    try {
      await deleteRestaurant(restaurantToDelete._id.$oid);
      await loadRestaurants();
      setDeleteDialogOpen(false);
      setRestaurantToDelete(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const confirmDelete = (restaurant) => {
    setRestaurantToDelete(restaurant);
    setDeleteDialogOpen(true);
  };

  const renderStars = (rating) => {
    return (
      <div className="flex items-center">
        {[...Array(5)].map((_, index) => (
          <Star
            key={index}
            size={16}
            className={index < rating ? "fill-yellow-400 text-yellow-400" : "text-gray-300"}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="container mx-auto p-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">Restaurant Directory</h1>
        
        {/* Search and Filter Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="flex items-center gap-2">
            <input
              type="text"
              placeholder="Search by city..."
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
            />
            <Search className="text-gray-400" />
          </div>
          
          <select
            value={priceRange}
            onChange={(e) => setPriceRange(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="">All Price Ranges</option>
            <option value="1">$ (Inexpensive)</option>
            <option value="2">$$ (Moderate)</option>
            <option value="3">$$$ (Expensive)</option>
            <option value="4">$$$$ (Very Expensive)</option>
          </select>

          <button
            onClick={handleAddNew}
            className="flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            <Plus className="mr-2" />
            Add Restaurant
          </button>
        </div>

        {/* Advanced Filters */}
        <AdvancedFilters onFilterChange={handleAdvancedFilters} />

        {/* Restaurant Cards */}
        {loading ? (
          <LoadingSpinner />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {restaurants.map((restaurant) => (
              <div
                key={restaurant._id.$oid}
                className="bg-white rounded-lg shadow-md overflow-hidden"
              >
                <div className="p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold">{restaurant.name}</h3>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(restaurant)}
                        className="p-1 hover:bg-gray-100 rounded"
                      >
                        <Edit2 size={16} />
                      </button>
                      <button
                        onClick={() => confirmDelete(restaurant)}
                        className="p-1 hover:bg-gray-100 rounded text-red-600"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center mb-2">
                    {renderStars(restaurant.stars)}
                    <span className="text-sm text-gray-500">
                      {restaurant.review_count} reviews
                    </span>
                  </div>
                  
                  <p className="text-gray-600 text-sm mb-2">
                    {restaurant.address}, {restaurant.city}, {restaurant.state}
                  </p>
                  
                  <p className="text-gray-500 text-sm mb-2">{restaurant.categories}</p>
                  
                  <div className="flex flex-wrap gap-2">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                      {'$'.repeat(parseInt(restaurant.attributes?.RestaurantsPriceRange2) || 1)}
                    </span>
                    {restaurant.attributes?.WiFi && (
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                        WiFi: {restaurant.attributes.WiFi}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        <div className="flex justify-center items-center space-x-4 mt-8">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Previous
          </button>
          <span>
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>

      {/* Restaurant Modal */}
      <RestaurantModal 
        isOpen={modalOpen}
        onClose={(shouldRefresh) => {
          setModalOpen(false);
          if (shouldRefresh) loadRestaurants();
        }}
        restaurant={selectedRestaurant}
        mode={modalMode}
      />

      {/* Delete Confirmation Dialog */}
      {deleteDialogOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg max-w-sm">
            <h3 className="text-lg font-semibold mb-4">Delete Restaurant</h3>
            <p>Are you sure you want to delete "{restaurantToDelete?.name}"?</p>
            <div className="flex justify-end space-x-4 mt-6">
              <button
                onClick={() => setDeleteDialogOpen(false)}
                className="px-4 py-2 border rounded"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Error Toast */}
      {error && <ErrorToast message={error} onClose={() => setError(null)} />}
    </div>
  );
};

export default RestaurantApp;