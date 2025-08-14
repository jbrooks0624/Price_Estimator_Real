"use client";

import React from "react";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";
import { ProcessDropdown, SkipButton, format } from "./VACommon";
import { PlusIcon, MinusIcon } from "@heroicons/react/24/outline";

const SlittingDropdown: React.FC<{
  validateCuts?: (cuts: Array<{ width: string; num: string }>) => boolean;
  updateSlitCut: (index: number, field: "width" | "num", value: string) => void;
  addSlitCut: () => void;
  deleteSlitCut: () => void;
}> = ({ updateSlitCut, addSlitCut, deleteSlitCut }) => {
  const { state, setState } = useSidebarState();
  return (
    <ProcessDropdown title="Slitting (Optional)">
      <SkipButton
        skipped={state.slitting.skipped}
        toggle={() =>
          setState((prev) => ({
            ...prev,
            slitting: { ...prev.slitting, skipped: !prev.slitting.skipped },
          }))
        }
      />
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium text-gray-800 mb-2">Cuts</h4>
          {state.slitting.cuts.map((cut, idx) => (
            <div key={idx} className="flex gap-4 mb-2">
              <div className="flex-1">
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Width Per Cut
                </label>
                <input
                  type="number"
                  min={0}
                  step="1"
                  inputMode="decimal"
                  value={cut.width}
                  onChange={(e) => updateSlitCut(idx, "width", e.target.value)}
                  onBlur={(e) =>
                    updateSlitCut(idx, "width", e.target.value, true)
                  }
                  disabled={state.slitting.skipped}
                  className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
                    state.slitting.skipped
                      ? "opacity-50 cursor-not-allowed"
                      : ""
                  }`}
                />
              </div>
              <div className="flex-1">
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  # Cuts
                </label>
                <input
                  type="number"
                  min={0}
                  step="1"
                  value={cut.num}
                  onChange={(e) => updateSlitCut(idx, "num", e.target.value)}
                  disabled={state.slitting.skipped}
                  className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
                    state.slitting.skipped
                      ? "opacity-50 cursor-not-allowed"
                      : ""
                  }`}
                />
              </div>
            </div>
          ))}
          <div className="flex justify-center gap-2 mt-2">
            <button
              type="button"
              onClick={addSlitCut}
              disabled={state.slitting.skipped}
              className="flex items-center gap-1 rounded border border-black px-2 py-1 text-xs hover:bg-gray-100 disabled:opacity-50"
            >
              <PlusIcon className="h-4 w-4" /> Add
            </button>
            {state.slitting.cuts.length > 1 && (
              <button
                type="button"
                onClick={deleteSlitCut}
                disabled={state.slitting.skipped}
                className="flex items-center gap-1 rounded border border-black px-2 py-1 text-xs hover:bg-gray-100 disabled:opacity-50"
              >
                <MinusIcon className="h-4 w-4" /> Delete
              </button>
            )}
          </div>
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
            value={state.slitting.cost}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                slitting: { ...prev.slitting, cost: e.target.value },
              }))
            }
            onBlur={(e) =>
              setState((prev) => ({
                ...prev,
                slitting: {
                  ...prev.slitting,
                  cost: format(e.target.value, 4),
                },
              }))
            }
            disabled={state.slitting.skipped}
            className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
              state.slitting.skipped ? "opacity-50 cursor-not-allowed" : ""
            }`}
          />
        </div>
      </div>
    </ProcessDropdown>
  );
};

export default SlittingDropdown;
