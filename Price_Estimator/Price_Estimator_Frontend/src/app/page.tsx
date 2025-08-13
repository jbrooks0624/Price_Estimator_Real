import type { Metadata } from "next";
import HomeInteractive from "@/components/HomeInteractive";

export const metadata: Metadata = {
  title: "Mainline Metals • Custom Price Calculator",
  description: "Instant pricing for your custom metal needs",
};

export default function Page() {
  return <HomeInteractive />;
}
