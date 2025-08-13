"use client";
import { useState } from "react";
import dynamic from "next/dynamic";
const Sidebar = dynamic(() => import("@/components/Sidebar"));
const SidebarToggle = dynamic(() => import("@/components/SidebarToggle"));
const ChatToggle = dynamic(() => import("@/components/ChatToggle"));
const ChatSidebar = dynamic(() => import("@/components/ChatSidebar"));
import { XMarkIcon, InformationCircleIcon } from "@heroicons/react/24/outline";
import SidebarContent from "@/components/SidebarContent";
import {
  useSidebarState,
  initialSidebarState,
} from "@/components/sidebarState/SidebarStateContext";
import {
  OutputProvider,
  useOutputState,
} from "@/components/OutputStateContext";

function HomePageInner() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [unitsOpen, setUnitsOpen] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const { state, setState } = useSidebarState();
  const { output, setOutput } = useOutputState();

  const sf = state.storageFreight;
  const num = (v: string) => {
    const parsed = parseFloat(v);
    return isNaN(parsed) ? 0 : parsed;
  };
  const numArr = (arr: string[]): number[] => arr.map((v) => num(v));
  const numPercent = (v: string) => num(v) / 100;

  const buildPayload = () => {
    return {
      // master
      master_coil_width: num(state.master.width),
      master_coil_weight: num(state.master.weight),
      master_coil_cost: num(state.master.cost),
      master_coil_thickness: num(state.master.thickness),
      master_coil_length: num(state.master.length),
      margin: num(state.master.margin),

      // examine
      examine_coil_scrap_percent: numPercent(state.examine.scrapPercent),
      examine_coil_cost: state.examine.cost,
      skip_examine_coil: state.examine.skipped,

      // trimming
      trimming_width_cropped: state.trimming.widthAfterTrim,
      trimming_cost: state.trimming.cost,
      skip_trimming: state.trimming.skipped,

      // pickle & oil
      pickle_scrap_percent: numPercent(state.pickleOil.scrapPercent),
      pickle_cost: state.pickleOil.cost,
      skip_pickle: state.pickleOil.skipped,

      // coating
      coating_scrap_percent: numPercent(state.coating.scrapPercent),
      coating_cost: state.coating.cost,
      skip_coating: state.coating.skipped,

      // slitting
      widths_per_cut: numArr(state.slitting.cuts.map((c) => c.width)),
      num_cuts_needed: state.slitting.cuts.map((c) => parseInt(c.num || "0")),
      slitting_cost: state.slitting.cost,
      skip_slitting: state.slitting.skipped,

      // cut to length
      cut_percent: numPercent(state.ctl.percent),
      cut_cost: state.ctl.cost,
      cut_weight: state.ctl.scrapWeight,
      skip_cut: state.ctl.skipped,

      // storage / freight
      storage_start: num(sf.start?.storage || "0"),
      freight_start: num(sf.start?.freight || "0"),
      storage_examine: num(sf.afterExamine?.storage || "0"),
      freight_examine: num(sf.afterExamine?.freight || "0"),
      storage_trimming: num(sf.afterTrimming?.storage || "0"),
      freight_trimming: num(sf.afterTrimming?.freight || "0"),
      storage_pickle: num(sf.afterPickle?.storage || "0"),
      freight_pickle: num(sf.afterPickle?.freight || "0"),
      storage_coating: num(sf.afterCoating?.storage || "0"),
      freight_coating: num(sf.afterCoating?.freight || "0"),
      storage_slitting: num(sf.afterSlitting?.storage || "0"),
      freight_slitting: num(sf.afterSlitting?.freight || "0"),
      storage_cut: num(sf.afterCTL?.storage || "0"),
      freight_cut: num(sf.afterCTL?.freight || "0"),
      storage_end: num(sf.end?.storage || "0"),
      freight_end: num(sf.end?.freight || "0"),

      // ctl2 (structured)
      ctl2: state.ctl2.skipped
        ? undefined
        : {
            skipped: state.ctl2.skipped,
            segments: state.ctl2.segments.map((s) => ({
              mode: s.mode,
              length: num(s.length || "0"),
              percent: s.mode === "percent" ? num(s.percent || "0") : undefined,
              pieces:
                s.mode === "pieces"
                  ? (() => {
                      const n = parseInt((s.pieces || "0").toString(), 10);
                      return isNaN(n) ? 0 : n;
                    })()
                  : undefined,
              action: s.action,
            })),
          },
    };
  };

  const runCalculator = async () => {
    try {
      const apiBase =
        process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
      const resp = await fetch(`${apiBase}/estimate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(buildPayload()),
      });
      const data = await resp.json();
      setOutput({ raw: data });
    } catch (err) {
      console.error(err);
    }
  };

  const formatValue = (
    label: string,
    v: number | string | null | undefined
  ) => {
    if (v === null || v === undefined) return "-";
    const lower = label.toLowerCase();
    const isWeight = lower.includes("weight");
    const isPercent = lower.includes("percent");
    const dec = isWeight || isPercent ? 2 : 4;
    const num = typeof v === "number" ? v : parseFloat(v);
    if (isNaN(num)) return String(v);
    return num.toFixed(dec);
  };

  const [calcOpen, setCalcOpen] = useState(false);
  const StatBox = ({
    title,
    items,
  }: {
    title: string;
    items: { label: string; value: number | string | null | undefined }[];
  }) => (
    <div className="relative border rounded-md p-4 flex-1 min-w-[220px] max-w-[250px] bg-white shadow">
      {/* info button */}
      <div className="absolute right-2 top-2 group">
        <button
          type="button"
          aria-label="View calculations"
          onClick={() => setCalcOpen(true)}
          className="h-5 w-5 flex items-center justify-center text-gray-600 hover:text-black"
        >
          <InformationCircleIcon className="h-5 w-5" />
        </button>
        <span className="absolute right-full mr-2 top-1/2 -translate-y-1/2 whitespace-nowrap rounded bg-gray-800 text-white text-xs px-2 py-1 opacity-0 group-hover:opacity-100 pointer-events-none">
          View Calculations
        </span>
      </div>
      <h3 className="font-semibold mb-2 text-gray-800 text-center">{title}</h3>
      <ul className="text-sm space-y-1">
        {items.map(({ label, value }) => (
          <li key={label} className="flex justify-between">
            <span className="text-gray-600">{label}</span>
            <span className="font-medium text-gray-900">
              {formatValue(label, value)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 relative">
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onInfo={() => setUnitsOpen(true)}
      >
        <SidebarContent />
      </Sidebar>

      <ChatSidebar open={chatOpen} onClose={() => setChatOpen(false)}>
        <p className="p-4 text-center text-sm text-gray-700">
          Chat coming soon...
        </p>
      </ChatSidebar>

      {/* Settings sidebar toggle */}
      {!sidebarOpen && (
        <SidebarToggle
          onClick={() => {
            setChatOpen(false);
            setSidebarOpen(true);
          }}
        />
      )}

      {/* Chat sidebar toggle */}
      {!chatOpen && (
        <ChatToggle
          onClick={() => {
            setSidebarOpen(false);
            setChatOpen(true);
          }}
        />
      )}

      <div
        className={`transition-all duration-300 ease-in-out px-4 pt-16 text-center ${
          sidebarOpen
            ? "ml-80 md:ml-[33.333%]"
            : chatOpen
            ? "mr-80 md:mr-[25%]"
            : ""
        }`}
      >
        <h1 className="text-3xl sm:text-5xl font-semibold text-gray-900">
          Mainline Metals
        </h1>
        <h2 className="mt-3 text-base sm:text-xl text-gray-700">
          Custom Price Calculator
        </h2>

        <div className="mt-6 flex justify-center">
          <button
            type="button"
            onClick={runCalculator}
            className="inline-flex items-center justify-center gap-2 rounded-md bg-blue-600 px-6 py-2 text-sm font-medium text-white shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            Run Calculator
          </button>
        </div>
        <div className="mt-2 flex justify-center gap-3">
          <button
            type="button"
            onClick={() => setOutput({ raw: null })}
            className="inline-flex items-center justify-center gap-1 rounded-md border border-blue-600 px-4 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50 focus:outline-none focus:ring-1 focus:ring-blue-400"
          >
            Clear Estimate
          </button>
          <button
            type="button"
            onClick={() => {
              setState(initialSidebarState);
              console.log("Parameters reset");
            }}
            className="inline-flex items-center justify-center gap-1 rounded-md border border-gray-600 px-4 py-1 text-xs font-medium text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-1 focus:ring-gray-400"
          >
            Reset Parameters
          </button>
        </div>

        {output.raw && (
          <>
            <div className="mt-6 flex flex-wrap justify-center gap-4">
              {/* Start Box */}
              <StatBox
                title="Start"
                items={[
                  { label: "Storage", value: output.raw.storage_at_start },
                  { label: "Freight", value: output.raw.freight_at_start },
                  {
                    label: "Running Cost",
                    value: output.raw.running_cost_after_start,
                  },
                ]}
              />

              {/* Conditional Process Boxes */}
              {!state.examine.skipped && (
                <StatBox
                  title="Examine Coil"
                  items={[
                    { label: "Cost", value: output.raw.cost_to_examine_coil },
                    {
                      label: "Scrap Weight",
                      value: output.raw.examine_scrap_weight,
                    },
                    {
                      label: "Storage",
                      value: output.raw.storage_after_examine,
                    },
                    {
                      label: "Freight",
                      value: output.raw.freight_after_examine,
                    },
                    {
                      label: "Running Cost",
                      value: output.raw.running_cost_after_examine,
                    },
                  ]}
                />
              )}

              {!state.trimming.skipped && (
                <StatBox
                  title="Trimming"
                  items={[
                    { label: "Cost", value: output.raw.cost_to_trim },
                    {
                      label: "Scrap Weight",
                      value: output.raw.trimming_scrap_weight,
                    },
                    {
                      label: "Storage",
                      value: output.raw.storage_after_trimming,
                    },
                    {
                      label: "Freight",
                      value: output.raw.freight_after_trimming,
                    },
                    {
                      label: "Running Cost",
                      value: output.raw.running_cost_after_trimming,
                    },
                  ]}
                />
              )}

              {!state.pickleOil.skipped && (
                <StatBox
                  title="Pickle & Oil"
                  items={[
                    { label: "Cost", value: output.raw.cost_to_pickle_and_oil },
                    {
                      label: "Scrap Weight",
                      value: output.raw.pickle_scrap_weight,
                    },
                    {
                      label: "Storage",
                      value: output.raw.storage_after_pickle,
                    },
                    {
                      label: "Freight",
                      value: output.raw.freight_after_pickle,
                    },
                    {
                      label: "Running Cost",
                      value: output.raw.running_cost_after_pickle,
                    },
                  ]}
                />
              )}

              {!state.coating.skipped && (
                <StatBox
                  title="Coating"
                  items={[
                    { label: "Cost", value: output.raw.cost_to_coat },
                    {
                      label: "Scrap Weight",
                      value: output.raw.coating_scrap_weight,
                    },
                    {
                      label: "Storage",
                      value: output.raw.storage_after_coating,
                    },
                    {
                      label: "Freight",
                      value: output.raw.freight_after_coating,
                    },
                    {
                      label: "Running Cost",
                      value: output.raw.running_cost_after_coating,
                    },
                  ]}
                />
              )}

              {!state.slitting.skipped && (
                <StatBox
                  title="Slitting"
                  items={[
                    { label: "Cost", value: output.raw.cost_to_slit },
                    {
                      label: "Scrap Weight",
                      value: output.raw.slitting_scrap_weight,
                    },
                    {
                      label: "Storage",
                      value: output.raw.storage_after_slitting,
                    },
                    {
                      label: "Freight",
                      value: output.raw.freight_after_slitting,
                    },
                    {
                      label: "Running Cost",
                      value: output.raw.running_cost_after_slitting,
                    },
                  ]}
                />
              )}

              {!state.ctl.skipped && (
                <StatBox
                  title="Cut to Length"
                  items={[
                    { label: "Cost", value: output.raw.cost_to_cut_to_length },
                    {
                      label: "Scrap Weight",
                      value: output.raw.cut_scrap_weight,
                    },
                    { label: "Storage", value: output.raw.storage_after_cut },
                    { label: "Freight", value: output.raw.freight_after_cut },
                    {
                      label: "Running Cost",
                      value: output.raw.running_cost_after_cut,
                    },
                  ]}
                />
              )}

              {/* End Box */}
              <StatBox
                title="End"
                items={[
                  { label: "Storage", value: output.raw.storage_at_end },
                  { label: "Freight", value: output.raw.freight_at_end },
                ]}
              />
            </div>

            {/* Summary Section */}
            <div className="mt-8 mx-auto max-w-md text-center bg-white p-6 rounded-md shadow">
              <h3 className="text-xl font-semibold mb-4">Summary</h3>
              <div className="space-y-1 text-left">
                <div className="flex justify-between">
                  <span>Total Cost</span>
                  <span>
                    {formatValue("Total Cost", output.raw.total_cost)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Final Weight</span>
                  <span>
                    {formatValue("Final Weight", output.raw.final_weight)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Scrap Percent</span>
                  <span>
                    {formatValue("Scrap Percent", output.raw.scrap_percent)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Scrap Weight</span>
                  <span>
                    {formatValue("Scrap Weight", output.raw.scrap_weight)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Selling Price</span>
                  <span>
                    {formatValue("Selling Price", output.raw.selling_price)}
                  </span>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Units Modal */}
      {(unitsOpen || calcOpen) && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="bg-white rounded-md shadow-lg w-11/12 max-w-md p-6 relative">
            {/* Close */}
            <button
              type="button"
              aria-label="Close units modal"
              onClick={() => {
                setUnitsOpen(false);
                setCalcOpen(false);
              }}
              className="absolute top-2 left-2 h-8 w-8 flex items-center justify-center rounded hover:bg-gray-200"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
            <h3 className="text-xl font-semibold mb-4 text-center">
              {unitsOpen ? "Units" : "Calculations"}
            </h3>
            {unitsOpen ? (
              <ul className="text-sm text-gray-700 list-disc pl-6 space-y-2 text-left">
                <li>
                  All <span className="font-medium">weights</span> are entered
                  in <span className="font-medium">hundred&nbsp;pounds</span>.
                </li>
                <li>
                  All <span className="font-medium">widths and lengths</span>{" "}
                  are in <span className="font-medium">inches</span>.
                </li>
                <li>
                  All <span className="font-medium">costs</span> are in{" "}
                  <span className="font-medium">
                    dollars per hundred&nbsp;pounds
                  </span>
                  .
                </li>
                <li>
                  <span className="font-medium">Length</span> is computed as{" "}
                  <span className="font-medium">
                    weight ÷ (width × thickness × density)
                  </span>
                  , with density = <code>0.2836</code>.
                </li>
                <li>
                  All <span className="font-medium">percent</span> inputs
                  represent the percentage value:
                  <br />
                  &nbsp;&nbsp;• <code>15.00</code> means <code>15% </code> (0.15
                  as a decimal).
                  <br />
                  &nbsp;&nbsp;• <code>0.15</code> means <code>0.15% </code>{" "}
                  (0.0015 as a decimal).
                </li>
              </ul>
            ) : (
              <p className="text-sm text-gray-700 text-center">
                Feature coming soon ...
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

import { SidebarStateProvider } from "@/components/sidebarState/SidebarStateContext";

export default function HomeInteractive() {
  return (
    <SidebarStateProvider>
      <OutputProvider>
        <HomePageInner />
      </OutputProvider>
    </SidebarStateProvider>
  );
}
