"use client";

import React from "react";
import { ProcessDropdown, SkipButton, format } from "./VACommon";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";

type CTL2Mode = "percent" | "pieces";
type CTL2Action = "scrap" | "restock" | "level";
type Segment = {
  mode: CTL2Mode;
  length: string;
  percent?: string;
  pieces?: string;
  action: CTL2Action;
};

const TogglePill: React.FC<{
  label: string;
  active: boolean;
  onClick: () => void;
}> = ({ label, active, onClick }) => (
  <button
    type="button"
    onClick={onClick}
    className={`px-3 py-1 rounded-full border text-sm transition-colors ${
      active
        ? "bg-black text-white border-black"
        : "bg-white text-black border-black hover:bg-gray-100"
    }`}
  >
    {label}
  </button>
);

const CutToLength2Dropdown: React.FC = () => {
  const { state, setState } = useSidebarState();
  const skipped = state.ctl2.skipped;
  const segments = state.ctl2.segments as Segment[];
  const effectiveSegments: Segment[] =
    segments && segments.length > 0
      ? segments
      : [{ mode: "percent", length: "", percent: "", action: "scrap" }];

  const setSkipped = (next: boolean) =>
    setState((prev) => ({ ...prev, ctl2: { ...prev.ctl2, skipped: next } }));

  const writeSegments = (nextSegments: Segment[]) =>
    setState((prev) => ({
      ...prev,
      ctl2: { ...prev.ctl2, segments: nextSegments },
    }));

  return (
    <ProcessDropdown title="Cut To Length 2.0 (Optional)">
      <SkipButton skipped={skipped} toggle={() => setSkipped(!skipped)} />
      <div className="space-y-4">
        {effectiveSegments.map((seg, idx) => (
          <div
            key={idx}
            className={idx > 0 ? "pt-3 border-t border-gray-200" : ""}
          >
            {/* Mode selector */}
            <div className="flex items-center justify-center gap-2">
              <TogglePill
                label="Length + Percent"
                active={seg.mode === "percent"}
                onClick={() => {
                  if (skipped) return;
                  const copy = [...effectiveSegments];
                  copy[idx] = { ...copy[idx], mode: "percent" };
                  writeSegments(copy);
                }}
              />
              <TogglePill
                label="Length + Pieces"
                active={seg.mode === "pieces"}
                onClick={() => {
                  if (skipped) return;
                  const copy = [...effectiveSegments];
                  copy[idx] = { ...copy[idx], mode: "pieces" };
                  writeSegments(copy);
                }}
              />
            </div>

            {/* Shared: Length */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Length (inches)
              </label>
              <input
                type="number"
                min={0}
                step="1"
                value={seg.length}
                onChange={(e) => {
                  const copy = [...effectiveSegments];
                  copy[idx] = {
                    ...copy[idx],
                    length: format(e.target.value, 4),
                  };
                  writeSegments(copy);
                }}
                disabled={skipped}
                className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
                  skipped ? "opacity-50 cursor-not-allowed" : ""
                }`}
              />
            </div>

            {/* Mode-specific input */}
            {seg.mode === "percent" ? (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Percent (%)
                </label>
                <input
                  type="number"
                  min={0}
                  step="1"
                  value={seg.percent || ""}
                  onChange={(e) => {
                    const copy = [...effectiveSegments];
                    copy[idx] = {
                      ...copy[idx],
                      percent: format(e.target.value, 2),
                      pieces: undefined,
                    };
                    writeSegments(copy);
                  }}
                  disabled={skipped}
                  className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
                    skipped ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                />
              </div>
            ) : (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Number of Pieces
                </label>
                <input
                  type="number"
                  min={0}
                  step="1"
                  value={seg.pieces || ""}
                  onChange={(e) => {
                    const copy = [...effectiveSegments];
                    copy[idx] = {
                      ...copy[idx],
                      pieces: e.target.value,
                      percent: undefined,
                    };
                    writeSegments(copy);
                  }}
                  disabled={skipped}
                  className={`block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black ${
                    skipped ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                />
              </div>
            )}

            <p className="text-xs text-gray-600">
              Choose one method: enter a length and either a percent or a number
              of pieces.
            </p>

            {/* Action (required) */}
            <div className="pt-2">
              <h4 className="text-sm font-medium text-gray-800 mb-2 text-center">
                Action (required)
              </h4>
              <div className="flex items-center justify-center gap-2">
                <TogglePill
                  label="Scrap"
                  active={seg.action === "scrap"}
                  onClick={() => {
                    if (skipped) return;
                    const copy = [...effectiveSegments];
                    copy[idx] = { ...copy[idx], action: "scrap" };
                    writeSegments(copy.slice(0, idx + 1));
                  }}
                />
                <TogglePill
                  label="Restock"
                  active={seg.action === "restock"}
                  onClick={() => {
                    if (skipped) return;
                    const copy = [...effectiveSegments];
                    copy[idx] = { ...copy[idx], action: "restock" };
                    writeSegments(copy.slice(0, idx + 1));
                  }}
                />
                <TogglePill
                  label="Level to Balance"
                  active={seg.action === "level"}
                  onClick={() => {
                    if (skipped) return;
                    const copy = [...effectiveSegments];
                    copy[idx] = { ...copy[idx], action: "level" };
                    if (idx === copy.length - 1) {
                      copy.push({
                        mode: "percent",
                        length: "",
                        percent: "",
                        action: "scrap",
                      });
                    }
                    writeSegments(copy);
                  }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </ProcessDropdown>
  );
};

export default CutToLength2Dropdown;
