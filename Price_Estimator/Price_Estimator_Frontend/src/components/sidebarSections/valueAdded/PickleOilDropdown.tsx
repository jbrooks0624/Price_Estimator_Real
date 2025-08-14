"use client";

import React from "react";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";
import { ProcessDropdown, SkipButton, format } from "./VACommon";

const PickleOilDropdown: React.FC = () => {
  const { state, setState } = useSidebarState();
  return (
    <ProcessDropdown title="Pickle & Oil (Optional)">
      <SkipButton
        skipped={state.pickleOil.skipped}
        toggle={() =>
          setState((prev) => ({
            ...prev,
            pickleOil: { ...prev.pickleOil, skipped: !prev.pickleOil.skipped },
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
            value={state.pickleOil.scrapPercent}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                pickleOil: {
                  ...prev.pickleOil,
                  scrapPercent: e.target.value,
                },
              }))
            }
            onBlur={(e) =>
              setState((prev) => ({
                ...prev,
                pickleOil: {
                  ...prev.pickleOil,
                  scrapPercent: format(e.target.value, 2),
                },
              }))
            }
            disabled={state.pickleOil.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.pickleOil.skipped ? "opacity-50 cursor-not-allowed" : ""
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
            value={state.pickleOil.cost}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                pickleOil: {
                  ...prev.pickleOil,
                  cost: e.target.value,
                },
              }))
            }
            onBlur={(e) =>
              setState((prev) => ({
                ...prev,
                pickleOil: {
                  ...prev.pickleOil,
                  cost: format(e.target.value, 4),
                },
              }))
            }
            disabled={state.pickleOil.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.pickleOil.skipped ? "opacity-50 cursor-not-allowed" : ""
            }`}
          />
        </div>
      </div>
    </ProcessDropdown>
  );
};

export default PickleOilDropdown;
