// src/utils/api.js

const API_BASE_URL = 'http://localhost:5001';

export const fetchRestaurants = async (params = {}) => {
  const queryParams = new URLSearchParams();
  
  // Basic filters
  if (params.name) queryParams.append('name', params.name);
  if (params.city) queryParams.append('city', params.city);
  if (params.price_range_min) queryParams.append('price_range_min', params.price_range_min);
  if (params.categories) queryParams.append('categories', params.categories);
  
  // Advanced filters
  if (params.wifi) queryParams.append('wifi', params.wifi);
  if (params.alcohol) queryParams.append('alcohol', params.alcohol);
  if (params.delivery) queryParams.append('delivery', params.delivery);
  if (params.pets_allowed) queryParams.append('pets_allowed', params.pets_allowed);
  if (params.parking) queryParams.append('parking', JSON.stringify(params.parking));
  if (params.smoking) queryParams.append('smoking', params.smoking);
  if (params.minStars) queryParams.append('minStars', params.minStars);
  
  // Pagination and sorting
  if (params.page) queryParams.append('page', params.page);
  if (params.per_page) queryParams.append('per_page', params.per_page);
  if (params.sort) queryParams.append('sort', params.sort);
  if (params.order) queryParams.append('order', params.order);

  const response = await fetch(`${API_BASE_URL}/api/restaurants?${queryParams}`);
  if (!response.ok) {
    throw new Error('Failed to fetch restaurants');
  }
  return response.json();
};

export const createRestaurant = async (data) => {
  const response = await fetch(`${API_BASE_URL}/api/restaurants`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to create restaurant');
  }
  return response.json();
};

export const updateRestaurant = async (id, data) => {
  const response = await fetch(`${API_BASE_URL}/api/restaurants/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to update restaurant');
  }
  return response.json();
};

export const deleteRestaurant = async (id) => {
  const response = await fetch(`${API_BASE_URL}/api/restaurants/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('Failed to delete restaurant');
  }
  return response.json();
};

export const fetchCategories = async () => {
  const response = await fetch(`${API_BASE_URL}/api/categories`);
  if (!response.ok) {
    throw new Error('Failed to fetch categories');
  }
  return response.json();
};