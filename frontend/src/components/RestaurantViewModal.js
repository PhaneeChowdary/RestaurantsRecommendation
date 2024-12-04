import React from 'react';
import { Star, MapPin, Clock, Wifi, Wine, Car, Dog } from 'lucide-react';

const RestaurantViewModal = ({ isOpen, onClose, restaurant }) => {
  if (!isOpen || !restaurant) return null;

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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-2xl font-bold">{restaurant.name}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ×
          </button>
        </div>

        <div className="space-y-6">
          {/* Rating and Reviews */}
          <div className="flex items-center gap-4">
            {renderStars(restaurant.stars)}
            <span className="text-gray-600">
              {restaurant.review_count} reviews
            </span>
          </div>

          {/* Location */}
          <div className="flex items-start gap-2">
            <MapPin className="mt-1 text-gray-400" size={18} />
            <div>
              <p>{restaurant.address}</p>
              <p>{restaurant.city}, {restaurant.state}</p>
            </div>
          </div>

          {/* Categories */}
          <div className="flex flex-wrap gap-2">
            {restaurant.categories?.split(',').map((category, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-gray-100 rounded-full text-sm"
              >
                {category.trim()}
              </span>
            ))}
          </div>

          {/* Attributes */}
          <div className="grid grid-cols-2 gap-4">
            {/* Price Range */}
            <div className="flex items-center gap-2">
              <span className="text-green-600 font-semibold">
                {'$'.repeat(parseInt(restaurant.attributes?.RestaurantsPriceRange2) || 1)}
              </span>
            </div>

            {/* WiFi */}
            {restaurant.attributes?.WiFi && (
              <div className="flex items-center gap-2">
                <Wifi size={18} className="text-blue-500" />
                <span>WiFi: {restaurant.attributes.WiFi}</span>
              </div>
            )}

            {/* Alcohol */}
            {restaurant.attributes?.Alcohol && (
              <div className="flex items-center gap-2">
                <Wine size={18} className="text-purple-500" />
                <span>{restaurant.attributes.Alcohol}</span>
              </div>
            )}

            {/* Parking */}
            {restaurant.attributes?.BusinessParking && (
              <div className="flex items-center gap-2">
                <Car size={18} className="text-gray-500" />
                <span>Parking Available</span>
              </div>
            )}

            {/* Dogs Allowed */}
            {restaurant.attributes?.DogsAllowed && (
              <div className="flex items-center gap-2">
                <Dog size={18} className="text-brown-500" />
                <span>Dogs Allowed</span>
              </div>
            )}
          </div>

          {/* Hours */}
          {restaurant.hours && (
            <div className="border-t pt-4">
              <h3 className="font-semibold mb-2 flex items-center gap-2">
                <Clock size={18} />
                Hours
              </h3>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(restaurant.hours).map(([day, hours]) => (
                  <div key={day} className="flex justify-between">
                    <span className="font-medium">{day}</span>
                    <span>{hours}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RestaurantViewModal;