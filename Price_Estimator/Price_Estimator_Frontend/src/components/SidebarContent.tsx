"use client";

import React from "react";
import dynamic from "next/dynamic";
const MasterCoilInfoSection = dynamic(
  () => import("@/components/sidebarSections/MasterCoilInfoSection")
);
const StorageFreightSection = dynamic(
  () => import("@/components/sidebarSections/StorageFreightSection")
);
const ValueAddedProcessesSection = dynamic(
  () => import("@/components/sidebarSections/ValueAddedProcessesSection")
);

/**
 * Aggregates all sidebar sections in order with dividers.
 */
const SidebarContent: React.FC = () => {
  return (
    <div>
      <MasterCoilInfoSection />
      <hr className="border-t border-gray-300 my-4" />
      <ValueAddedProcessesSection />
      <hr className="border-t border-gray-300 my-4" />
      <StorageFreightSection />
    </div>
  );
};

export default SidebarContent;
