"use client";

import React, { useState } from "react";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/24/outline";
import ExamineDropdown from "@/components/sidebarSections/valueAdded/ExamineDropdown";
import TrimmingDropdown from "@/components/sidebarSections/valueAdded/TrimmingDropdown";
import PickleOilDropdown from "@/components/sidebarSections/valueAdded/PickleOilDropdown";
import CoatingDropdown from "@/components/sidebarSections/valueAdded/CoatingDropdown";
import SlittingDropdown from "@/components/sidebarSections/valueAdded/SlittingDropdown";
import CutToLengthDropdown from "./valueAdded/CutToLengthDropdown";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";

const ValueAddedProcessesSection: React.FC = () => {
  const { state, setState } = useSidebarState();

  const getMasterWidth = () => parseFloat(state.master.width || "0");
  const validateCuts = (
    cuts: Array<{ width: string; num: string }>
  ): boolean => {
    const total = cuts.reduce(
      (sum, c) => sum + parseFloat(c.width || "0") * parseInt(c.num || "0"),
      0
    );
    return total <= getMasterWidth();
  };

  const updateSlitCut = (
    index: number,
    field: "width" | "num",
    value: string,
    commit: boolean = false
  ) => {
    setState((prev) => {
      const cutsCopy = [...prev.slitting.cuts];
      if (field === "width") {
        cutsCopy[index] = {
          ...cutsCopy[index],
          width:
            commit && value !== ""
              ? parseFloat(value || "0").toFixed(4)
              : value,
        };
      } else {
        cutsCopy[index] = { ...cutsCopy[index], num: value };
      }
      if (!validateCuts(cutsCopy)) return prev;
      return { ...prev, slitting: { ...prev.slitting, cuts: cutsCopy } };
    });
  };

  const addSlitCut = () => {
    setState((prev) => {
      const candidate = [...prev.slitting.cuts, { width: "0.0000", num: "1" }];
      if (!validateCuts(candidate)) return prev;
      return { ...prev, slitting: { ...prev.slitting, cuts: candidate } };
    });
  };

  const deleteSlitCut = () => {
    setState((prev) => {
      if (prev.slitting.cuts.length <= 1) return prev;
      const candidate = prev.slitting.cuts.slice(0, -1);
      if (!validateCuts(candidate)) return prev;
      return { ...prev, slitting: { ...prev.slitting, cuts: candidate } };
    });
  };

  const [open, setOpen] = useState(false);

  return (
    <section className="mb-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-800">
          Value Added Processes
        </h3>
        <button
          type="button"
          aria-label="Toggle value added"
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
        <>
          <ExamineDropdown />
          <TrimmingDropdown />
          <PickleOilDropdown />
          <CoatingDropdown />
          <SlittingDropdown
            validateCuts={validateCuts}
            updateSlitCut={updateSlitCut}
            addSlitCut={addSlitCut}
            deleteSlitCut={deleteSlitCut}
          />
          <CutToLengthDropdown />
        </>
      )}
    </section>
  );
};

export default ValueAddedProcessesSection;
