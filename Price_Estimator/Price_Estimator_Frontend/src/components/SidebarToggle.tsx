"use client";
import { Cog6ToothIcon } from "@heroicons/react/24/outline";
import React from "react";

interface SidebarToggleProps {
  onClick: () => void;
}

/**
 * Floating circular button used to open the sidebar.
 */
const SidebarToggle: React.FC<SidebarToggleProps> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      aria-label="Open settings"
      className="fixed top-6 left-6 z-50 flex h-12 w-12 items-center justify-center rounded-full bg-white border-2 border-black p-2 text-black shadow hover:bg-gray-50"
    >
      <Cog6ToothIcon className="h-6 w-6" />
    </button>
  );
};

export default SidebarToggle;
