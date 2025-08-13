"use client";
import React, { createContext, useContext, useState } from "react";

export interface PriceEstimatorOutput {
  storage_at_start?: number | null;
  freight_at_start?: number | null;
  running_cost_after_start?: number | null;
  cost_to_examine_coil?: number | null;
  examine_scrap_weight?: number | null;
  storage_after_examine?: number | null;
  freight_after_examine?: number | null;
  running_cost_after_examine?: number | null;
  cost_to_trim?: number | null;
  trimming_scrap_weight?: number | null;
  storage_after_trimming?: number | null;
  freight_after_trimming?: number | null;
  running_cost_after_trimming?: number | null;
  cost_to_pickle_and_oil?: number | null;
  pickle_scrap_weight?: number | null;
  storage_after_pickle?: number | null;
  freight_after_pickle?: number | null;
  running_cost_after_pickle?: number | null;
  cost_to_coat?: number | null;
  coating_scrap_weight?: number | null;
  storage_after_coating?: number | null;
  freight_after_coating?: number | null;
  running_cost_after_coating?: number | null;
  cost_to_slit?: number | null;
  slitting_scrap_weight?: number | null;
  storage_after_slitting?: number | null;
  freight_after_slitting?: number | null;
  running_cost_after_slitting?: number | null;
  cost_to_cut_to_length?: number | null;
  cut_scrap_weight?: number | null;
  storage_after_cut?: number | null;
  freight_after_cut?: number | null;
  running_cost_after_cut?: number | null;
  storage_at_end?: number | null;
  freight_at_end?: number | null;
  total_cost?: number | null;
  final_weight?: number | null;
  scrap_percent?: number | null;
  scrap_weight?: number | null;
  selling_price?: number | null;
}

export interface OutputState {
  raw: PriceEstimatorOutput | null;
}

const OutputContext = createContext<
  | {
      output: OutputState;
      setOutput: React.Dispatch<React.SetStateAction<OutputState>>;
    }
  | undefined
>(undefined);

export const OutputProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [output, setOutput] = useState<OutputState>({ raw: null });
  return (
    <OutputContext.Provider value={{ output, setOutput }}>
      {children}
    </OutputContext.Provider>
  );
};

export const useOutputState = () => {
  const ctx = useContext(OutputContext);
  if (!ctx)
    throw new Error("useOutputState must be used within OutputProvider");
  return ctx;
};
