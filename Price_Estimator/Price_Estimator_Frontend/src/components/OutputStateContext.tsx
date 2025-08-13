"use client";
import React, { createContext, useContext, useState } from "react";

export interface OutputState {
  raw: any | null;
}

const OutputContext = createContext<{
  output: OutputState;
  setOutput: React.Dispatch<React.SetStateAction<OutputState>>;
} | undefined>(undefined);

export const OutputProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [output, setOutput] = useState<OutputState>({ raw: null });
  return <OutputContext.Provider value={{ output, setOutput }}>{children}</OutputContext.Provider>;
};

export const useOutputState = () => {
  const ctx = useContext(OutputContext);
  if (!ctx) throw new Error("useOutputState must be used within OutputProvider");
  return ctx;
};
