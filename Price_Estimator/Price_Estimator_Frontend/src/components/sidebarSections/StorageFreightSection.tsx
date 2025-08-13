"use client";

import React from "react";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/24/outline";
import { useSidebarState } from "@/components/sidebarState/SidebarStateContext";

const stages = [
  { key: "start", label: "At Start", visible: () => true },
  {
    key: "afterExamine",
    label: "After Examine",
    visible: (s: any) => !s.examine.skipped,
  },
  {
    key: "afterTrimming",
    label: "After Trimming",
    visible: (s: any) => !s.trimming.skipped,
  },
  {
    key: "afterPickle",
    label: "After Pickle & Oil",
    visible: (s: any) => !s.pickleOil.skipped,
  },
  {
    key: "afterCoating",
    label: "After Coating",
    visible: (s: any) => !s.coating.skipped,
  },
  {
    key: "afterSlitting",
    label: "After Slitting",
    visible: (s: any) => !s.slitting.skipped,
  },
  {
    key: "afterCTL",
    label: "After Cut To Length",
    visible: (s: any) => !s.ctl.skipped,
  },
  { key: "end", label: "At End", visible: () => true },
];

const StorageFreightSection: React.FC = () => {
  const { state, setState } = useSidebarState();
  const [open, setOpen] = React.useState(false);

  const update = (
    stageKey: string,
    field: "storage" | "freight",
    value: string
  ) => {
    setState((prev) => ({
      ...prev,
      storageFreight: {
        ...prev.storageFreight,
        [stageKey]: {
          storage:
            field === "storage"
              ? value
              : prev.storageFreight[stageKey]?.storage || "0.0000",
          freight:
            field === "freight"
              ? value
              : prev.storageFreight[stageKey]?.freight || "0.0000",
        },
      },
    }));
  };

  return (
    <section className="mb-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-800">
          Storage & Freight Costs
        </h3>
        <button
          type="button"
          aria-label="Toggle storage freight"
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
        <div className="space-y-3">
          <p className="text-sm font-semibold text-gray-700 mb-1">
            *Storage is in dollars per 100 pounds, Frieght is in dollars*
          </p>
          {stages
            .filter((st) => st.visible(state))
            .map((st) => {
              const row = state.storageFreight[st.key] || {
                storage: "0.0000",
                freight: "0.0000",
              };
              return (
                <div key={st.key}>
                  <p className="text-sm font-medium text-gray-700 mb-1">
                    {st.label}
                  </p>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs mb-0.5">Storage</label>
                      <input
                        type="number"
                        min={0}
                        step="0.1"
                        value={row.storage}
                        onChange={(e) =>
                          update(
                            st.key,
                            "storage",
                            parseFloat(e.target.value).toFixed(4)
                          )
                        }
                        className="block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black"
                      />
                    </div>
                    <div>
                      <label className="block text-xs mb-0.5">Freight</label>
                      <input
                        type="number"
                        min={0}
                        step="100"
                        value={row.freight}
                        onChange={(e) =>
                          update(
                            st.key,
                            "freight",
                            parseFloat(e.target.value).toFixed(4)
                          )
                        }
                        className="block w-full rounded-md border-2 border-black bg-white p-2 focus:border-black focus:ring-black"
                      />
                    </div>
                  </div>
                </div>
              );
            })}
        </div>
      )}
    </section>
  );
};

export default StorageFreightSection;
