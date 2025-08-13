"use client";

import React, { useState } from "react";
import {
  ChevronDownIcon,
  ChevronUpIcon,
  CheckIcon,
} from "@heroicons/react/24/outline";

export const format = (v: string, d: number) =>
  v === "" ? "" : parseFloat(v).toFixed(d);

export const ProcessDropdown: React.FC<{
  title: string;
  children?: React.ReactNode;
}> = ({ title, children }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-gray-300 rounded mb-3 overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between bg-gray-100 px-3 py-2 hover:bg-gray-200 focus:outline-none"
      >
        <span className="font-medium text-left text-gray-800">{title}</span>
        {open ? (
          <ChevronUpIcon className="h-5 w-5 text-gray-600" />
        ) : (
          <ChevronDownIcon className="h-5 w-5 text-gray-600" />
        )}
      </button>
      {open && <div className="p-4 bg-white">{children}</div>}
    </div>
  );
};

export const SkipButton: React.FC<{ skipped: boolean; toggle: () => void }> = ({
  skipped,
  toggle,
}) => (
  <div className="flex justify-center mb-4">
    <button
      type="button"
      onClick={toggle}
      className={`relative inline-flex w-28 items-center justify-center rounded-md border-2 px-3 py-1 text-sm font-medium transition-colors ${
        skipped
          ? "border-green-600 bg-green-100 text-green-700"
          : "border-gray-600 bg-white text-gray-800 hover:bg-gray-50"
      }`}
    >
      {skipped && <CheckIcon className="absolute left-2 h-4 w-4" />}
      <span className="mx-auto">Skip</span>
    </button>
  </div>
);
