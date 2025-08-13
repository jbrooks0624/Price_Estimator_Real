"use client";

import React, { createContext, useContext, useState } from "react";

type CTL2Mode = "percent" | "pieces";
type CTL2Action = "scrap" | "restock" | "level";

export type CTL2Segment = {
  mode: CTL2Mode;
  length: string; // inches, stored as string for consistency
  percent?: string; // when mode === "percent"
  pieces?: string; // when mode === "pieces"
  action: CTL2Action; // required action for the segment
};

export interface SidebarState {
  master: {
    width: string;
    weight: string;
    cost: string;
    margin: string;
    thickness: string;
    length: string; // computed, read-only in UI
  };
  examine: {
    skipped: boolean;
    scrapPercent: string;
    cost: string;
  };
  trimming: {
    skipped: boolean;
    widthAfterTrim: string;
    cost: string;
  };
  pickleOil: {
    skipped: boolean;
    scrapPercent: string;
    cost: string;
  };
  coating: {
    skipped: boolean;
    scrapPercent: string;
    cost: string;
  };
  slitting: {
    skipped: boolean;
    cuts: Array<{ width: string; num: string }>;
    cost: string;
  };
  ctl: {
    skipped: boolean;
    percent: string;
    scrapWeight: string;
    cost: string;
  };
  storageFreight: Record<string, { storage: string; freight: string }>;
  ctl2: {
    skipped: boolean;
    segments: CTL2Segment[];
  };
}

export const initialSidebarState: SidebarState = {
  master: {
    width: "48.0000",
    weight: "40000.00",
    cost: "100.0000",
    margin: "15.00",
    thickness: "0.0700",
    // Using formula: length = weight / (width x thickness x density), density=0.2836
    length: (() => {
      const density = 0.2836;
      const width = parseFloat("48.0000");
      const weight = parseFloat("40000.00");
      const thickness = parseFloat("0.0700");
      const denom = width * thickness * density;
      if (!isFinite(denom) || denom === 0) return "";
      const val = weight / denom;
      return isFinite(val) ? val.toFixed(2) : "";
    })(),
  },
  examine: { skipped: true, scrapPercent: "1.00", cost: "1.5000" },
  trimming: { skipped: true, widthAfterTrim: "47.0000", cost: "1.5000" },
  pickleOil: { skipped: true, scrapPercent: "1.00", cost: "1.5000" },
  coating: { skipped: true, scrapPercent: "1.00", cost: "10.0000" },
  slitting: {
    skipped: true,
    cuts: [{ width: "48.0000", num: "1" }],
    cost: "2.5000",
  },
  ctl: {
    skipped: true,
    percent: "20.00",
    scrapWeight: "150.00",
    cost: "1.5000",
  },
  storageFreight: {},
  ctl2: {
    skipped: true,
    segments: [],
  },
};

type SidebarContextType = {
  state: SidebarState;
  setState: React.Dispatch<React.SetStateAction<SidebarState>>;
};

export const SidebarStateContext = createContext<
  SidebarContextType | undefined
>(undefined);

export const SidebarStateProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [state, setState] = useState<SidebarState>(initialSidebarState);
  return (
    <SidebarStateContext.Provider value={{ state, setState }}>
      {children}
    </SidebarStateContext.Provider>
  );
};

export const useSidebarState = () => {
  const ctx = useContext(SidebarStateContext);
  if (!ctx)
    throw new Error("useSidebarState must be used within SidebarStateProvider");
  return ctx;
};
