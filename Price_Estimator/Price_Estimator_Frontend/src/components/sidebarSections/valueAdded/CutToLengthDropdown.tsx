"use client";

import React from "react";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";
import { ProcessDropdown, SkipButton, format } from "./VACommon";

const CutToLengthDropdown: React.FC = () => {
  const { state, setState } = useSidebarState();
  return (
    <ProcessDropdown title="Cut To Length (Optional)">
      <SkipButton
        skipped={state.ctl.skipped}
        toggle={() =>
          setState((prev) => ({
            ...prev,
            ctl: { ...prev.ctl, skipped: !prev.ctl.skipped },
          }))
        }
      />
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Cut To Length Percent
          </label>
          <input
            type="number"
            min={0}
            step="1"
            value={state.ctl.percent}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                ctl: { ...prev.ctl, percent: format(e.target.value, 2) },
              }))
            }
            disabled={state.ctl.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.ctl.skipped ? "opacity-50 cursor-not-allowed" : ""
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Scrap Weight
          </label>
          <input
            type="number"
            min={0}
            step="1"
            value={state.ctl.scrapWeight}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                ctl: { ...prev.ctl, scrapWeight: format(e.target.value, 2) },
              }))
            }
            disabled={state.ctl.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.ctl.skipped ? "opacity-50 cursor-not-allowed" : ""
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
            value={state.ctl.cost}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                ctl: { ...prev.ctl, cost: format(e.target.value, 4) },
              }))
            }
            disabled={state.ctl.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.ctl.skipped ? "opacity-50 cursor-not-allowed" : ""
            }`}
          />
        </div>
      </div>
    </ProcessDropdown>
  );
};

export default CutToLengthDropdown;
