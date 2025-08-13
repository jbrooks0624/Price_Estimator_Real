"use client";
import { XMarkIcon, InformationCircleIcon } from "@heroicons/react/24/outline";
import React from "react";

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  onInfo?: () => void;
  children?: React.ReactNode;
}

/**
 * Sliding sidebar that appears from the left.
 * Hidden with a negative translate when `open` is false.
 */
const Sidebar: React.FC<SidebarProps> = ({
  open,
  onClose,
  onInfo,
  children,
}) => {
  return (
    <aside
      className={`fixed inset-y-0 left-0 z-40 w-80 md:w-1/3 bg-gray-100 shadow-lg transform transition-transform duration-300 ease-in-out
        ${open ? "translate-x-0" : "-translate-x-full"}`}
    >
      {/* Close button */}
      <button
        onClick={onClose}
        aria-label="Close sidebar"
        className="absolute top-0 right-0 h-12 w-12 flex items-center justify-center rounded hover:bg-gray-200 z-20"
      >
        <XMarkIcon className="h-6 w-6 text-black" />
      </button>

      {/* Header */}
      <div className="absolute top-0 left-0 right-0 h-12 bg-gray-200 flex items-center justify-center gap-2 px-2">
        {/* Info button */}
        {onInfo && (
          <div className="absolute left-2 top-1/2 -translate-y-1/2 group">
            <button
              type="button"
              onClick={onInfo}
              aria-label="Units info"
              className="flex items-center justify-center h-8 w-8 rounded hover:bg-gray-300"
            >
              <InformationCircleIcon className="h-5 w-5 text-black" />
            </button>
            <span className="absolute left-full ml-2 top-1/2 -translate-y-1/2 whitespace-nowrap rounded bg-gray-800 text-white text-xs px-2 py-1 opacity-0 group-hover:opacity-100 pointer-events-none">
              View Units
            </span>
          </div>
        )}
        <h2 className="text-xl font-semibold">Parameters</h2>
      </div>

      {/* Scrollable content */}
      <div className="p-6 pt-16 h-full overflow-y-auto">{children}</div>
    </aside>
  );
};

export default Sidebar;
