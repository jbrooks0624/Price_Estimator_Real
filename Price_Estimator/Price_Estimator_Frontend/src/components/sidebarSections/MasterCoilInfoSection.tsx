"use client";

import React, { useState } from "react";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/24/outline";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";

/**
 * Master Coil Info section with collapsible functionality and shared state
 */
const MasterCoilInfoSection: React.FC = () => {
  const { state, setState } = useSidebarState();
  const master = state.master;
  // removed unused helper

  const format = (v: string, d: number) =>
    v === "" ? "" : parseFloat(v).toFixed(d);
  const [open, setOpen] = useState(true);

  // Derived: length = weight / (width x thickness x density)
  const density = 0.2836;
  const recomputeLength = (overrides?: Partial<typeof master>) => {
    const width = parseFloat((overrides?.width ?? master.width) || "0");
    const weight = parseFloat((overrides?.weight ?? master.weight) || "0");
    const thickness = parseFloat(
      (overrides?.thickness ?? master.thickness) || "0"
    );
    const denom = width * thickness * density;
    if (!isFinite(denom) || denom === 0) return "";
    const value = weight / denom;
    return isFinite(value) ? value.toFixed(2) : "";
  };

  return (
    <section className="mb-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-800">
          Master Coil Info
        </h3>
        <button
          type="button"
          aria-label="Toggle master coil info"
          onClick={() => setOpen(!open)}
          className="p-1"
        >
          {open ? (
            <ChevronUpIcon className="h-5 w-5 text-gray-600" />
          ) : (
            <ChevronDownIcon className="h-5 w-5 text-gray-600" />
          )}
        </button>
      </div>
      {open && (
        <div className="space-y-4">
          {/* Width */}
          <div>
            <label
              htmlFor="master-coil-width"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Master Coil Width
            </label>
            <input
              id="master-coil-width"
              type="number"
              min={0}
              step={1}
              inputMode="decimal"
              value={master.width}
              onChange={(e) => {
                const raw = e.target.value;
                const nextLength = recomputeLength({ width: raw });
                setState((prev) => ({
                  ...prev,
                  master: {
                    ...prev.master,
                    width: raw,
                    length: nextLength,
                  },
                }));
              }}
              onBlur={(e) => {
                const formatted = format(e.target.value, 4);
                const nextLength = recomputeLength({ width: formatted });
                setState((prev) => ({
                  ...prev,
                  master: {
                    ...prev.master,
                    width: formatted,
                    length: nextLength,
                  },
                }));
              }}
              className="block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black"
            />
          </div>

          {/* Weight */}
          <div>
            <label
              htmlFor="master-coil-weight"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Master Coil Weight
            </label>
            <input
              id="master-coil-weight"
              type="number"
              min={0}
              step={10}
              inputMode="decimal"
              value={master.weight}
              onChange={(e) => {
                const raw = e.target.value;
                const nextLength = recomputeLength({ weight: raw });
                setState((prev) => ({
                  ...prev,
                  master: {
                    ...prev.master,
                    weight: raw,
                    length: nextLength,
                  },
                }));
              }}
              onBlur={(e) => {
                const formatted = format(e.target.value, 2);
                const nextLength = recomputeLength({ weight: formatted });
                setState((prev) => ({
                  ...prev,
                  master: {
                    ...prev.master,
                    weight: formatted,
                    length: nextLength,
                  },
                }));
              }}
              className="block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black"
            />
          </div>

          {/* Cost */}
          <div>
            <label
              htmlFor="master-coil-cost"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Master Coil Cost
            </label>
            <input
              id="master-coil-cost"
              type="number"
              min={0}
              step={1}
              inputMode="decimal"
              value={master.cost}
              onChange={(e) => {
                const raw = e.target.value;
                setState((prev) => ({
                  ...prev,
                  master: { ...prev.master, cost: raw },
                }));
              }}
              onBlur={(e) => {
                const formatted = format(e.target.value, 4);
                setState((prev) => ({
                  ...prev,
                  master: { ...prev.master, cost: formatted },
                }));
              }}
              className="block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black"
            />
          </div>

          {/* Thickness (under cost) */}
          <div>
            <label
              htmlFor="master-coil-thickness"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Master Coil Thickness
            </label>
            <input
              id="master-coil-thickness"
              type="number"
              min={0}
              step={0.0001}
              inputMode="decimal"
              value={master.thickness}
              onChange={(e) => {
                const raw = e.target.value;
                const nextLength = recomputeLength({ thickness: raw });
                setState((prev) => ({
                  ...prev,
                  master: {
                    ...prev.master,
                    thickness: raw,
                    length: nextLength,
                  },
                }));
              }}
              onBlur={(e) => {
                const formatted = format(e.target.value, 4);
                const nextLength = recomputeLength({ thickness: formatted });
                setState((prev) => ({
                  ...prev,
                  master: {
                    ...prev.master,
                    thickness: formatted,
                    length: nextLength,
                  },
                }));
              }}
              className="block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black"
            />
          </div>

          {/* Length (computed, under cost/thickness) */}
          <div>
            <label
              htmlFor="master-coil-length"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Length (computed)
            </label>
            <input
              id="master-coil-length"
              type="text"
              readOnly
              value={master.length}
              className="block w-full rounded-md border-2 border-black bg-gray-100 p-2 text-gray-700"
            />
          </div>

          {/* Margin (after) */}
          <div>
            <label
              htmlFor="margin-percentage"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Margin (%)
            </label>
            <input
              id="margin-percentage"
              type="number"
              min={0}
              step={1}
              inputMode="decimal"
              value={master.margin}
              onChange={(e) => {
                const raw = e.target.value;
                setState((prev) => ({
                  ...prev,
                  master: { ...prev.master, margin: raw },
                }));
              }}
              onBlur={(e) => {
                const formatted = format(e.target.value, 2);
                setState((prev) => ({
                  ...prev,
                  master: { ...prev.master, margin: formatted },
                }));
              }}
              className="block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black"
            />
          </div>
        </div>
      )}
    </section>
  );
};

export default MasterCoilInfoSection;
