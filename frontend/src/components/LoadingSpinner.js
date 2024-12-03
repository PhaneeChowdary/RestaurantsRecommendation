import React from 'react';

const LoadingSpinner = () => (
  <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
    <div className="bg-white p-4 rounded-lg shadow-lg">
      <div className="flex items-center space-x-2">
        <div className="w-4 h-4 bg-blue-600 rounded-full animate-bounce" />
        <div className="w-4 h-4 bg-blue-600 rounded-full animate-bounce delay-100" />
        <div className="w-4 h-4 bg-blue-600 rounded-full animate-bounce delay-200" />
      </div>
      <p className="text-center mt-2">Loading...</p>
    </div>
  </div>
);

export default LoadingSpinner;