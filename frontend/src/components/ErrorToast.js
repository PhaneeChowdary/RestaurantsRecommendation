import React, { useEffect } from 'react';
import { X } from 'lucide-react';

const ErrorToast = ({ message, onClose, duration = 5000 }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [onClose, duration]);

  return (
    <div className="fixed bottom-4 right-4 z-50 animate-fade-in">
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md shadow-lg">
        <div className="flex items-start">
          <div className="flex-grow pr-8">
            <p className="font-medium">Error</p>
            <p className="text-sm mt-1">{message}</p>
          </div>
          <button 
            onClick={onClose}
            className="absolute top-2 right-2 text-red-700 hover:text-red-800"
          >
            <X size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

// Add animation keyframes to your global CSS or style tag
const style = document.createElement('style');
style.textContent = `
  @keyframes fade-in {
    from {
      opacity: 0;
      transform: translateY(1rem);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .animate-fade-in {
    animation: fade-in 0.3s ease-out;
  }
`;
document.head.appendChild(style);

export default ErrorToast;