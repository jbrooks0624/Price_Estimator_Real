"use client";

import React from "react";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";
import { ProcessDropdown, SkipButton, format } from "./VACommon";

const TrimmingDropdown: React.FC = () => {
  const { state, setState } = useSidebarState();
  return (
    <ProcessDropdown title="Trimming (Optional)">
      <SkipButton
        skipped={state.trimming.skipped}
        toggle={() =>
          setState((prev) => ({
            ...prev,
            trimming: { ...prev.trimming, skipped: !prev.trimming.skipped },
          }))
        }
      />
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Width After Trim
          </label>
          <input
            type="number"
            min={0}
            step="1"
            value={state.trimming.widthAfterTrim}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                trimming: {
                  ...prev.trimming,
                  widthAfterTrim: format(e.target.value, 4),
                },
              }))
            }
            disabled={state.trimming.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.trimming.skipped ? "opacity-50 cursor-not-allowed" : ""
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Cost
          </label>
          <input
            type="number"
            min={0}
            step="0.1"
            value={state.trimming.cost}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                trimming: { ...prev.trimming, cost: format(e.target.value, 4) },
              }))
            }
            disabled={state.trimming.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.trimming.skipped ? "opacity-50 cursor-not-allowed" : ""
            }`}
          />
        </div>
      </div>
    </ProcessDropdown>
  );
};

export default TrimmingDropdown;
