"use client";

import React from "react";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";
import { ProcessDropdown, SkipButton, format } from "./VACommon";

const ExamineDropdown: React.FC = () => {
  const { state, setState } = useSidebarState();
  return (
    <ProcessDropdown title="Examine Coil (Optional)">
      <SkipButton
        skipped={state.examine.skipped}
        toggle={() =>
          setState((prev) => ({
            ...prev,
            examine: { ...prev.examine, skipped: !prev.examine.skipped },
          }))
        }
      />
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Scrap Percent (%)
          </label>
          <input
            type="number"
            min={0}
            step="1"
            inputMode="decimal"
            value={state.examine.scrapPercent}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                examine: {
                  ...prev.examine,
                  scrapPercent: e.target.value,
                },
              }))
            }
            onBlur={(e) =>
              setState((prev) => ({
                ...prev,
                examine: {
                  ...prev.examine,
                  scrapPercent: format(e.target.value, 2),
                },
              }))
            }
            disabled={state.examine.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.examine.skipped ? "opacity-50 cursor-not-allowed" : ""
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
            inputMode="decimal"
            value={state.examine.cost}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                examine: { ...prev.examine, cost: e.target.value },
              }))
            }
            onBlur={(e) =>
              setState((prev) => ({
                ...prev,
                examine: { ...prev.examine, cost: format(e.target.value, 4) },
              }))
            }
            disabled={state.examine.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.examine.skipped ? "opacity-50 cursor-not-allowed" : ""
            }`}
          />
        </div>
      </div>
    </ProcessDropdown>
  );
};

export default ExamineDropdown;
