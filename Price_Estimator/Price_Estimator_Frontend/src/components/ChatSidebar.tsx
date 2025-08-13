"use client";
import { XMarkIcon } from "@heroicons/react/24/outline";
import React from "react";

interface ChatSidebarProps {
  open: boolean;
  onClose: () => void;
  children?: React.ReactNode;
}

/**
 * Sliding sidebar that appears from the right.
 * Hidden with a positive translate when `open` is false.
 */
const ChatSidebar: React.FC<ChatSidebarProps> = ({
  open,
  onClose,
  children,
}) => {
  return (
    <aside
      className={`fixed inset-y-0 right-0 z-40 w-80 md:w-1/4 bg-gray-100 shadow-lg transform transition-transform duration-300 ease-in-out ${
        open ? "translate-x-0" : "translate-x-full"
      }`}
    >
      {/* Close button */}
      <button
        onClick={onClose}
        aria-label="Close chat sidebar"
        className="absolute top-0 left-0 h-12 w-12 flex items-center justify-center rounded hover:bg-gray-200 z-20"
      >
        <XMarkIcon className="h-6 w-6 text-black" />
      </button>

      {/* Header */}
      <div className="absolute top-0 left-0 right-0 h-12 bg-gray-200 flex items-center justify-center px-2">
        <h2 className="text-xl font-semibold">Chat</h2>
      </div>

      {/* Scrollable content */}
      <div className="p-6 pt-16 h-full overflow-y-auto">
        {children ?? (
          <p className="text-center text-sm text-gray-700">
            Chat coming soon...
          </p>
        )}
      </div>
    </aside>
  );
};

export default ChatSidebar;
