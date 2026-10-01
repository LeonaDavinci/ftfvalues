import CategoryView from "@/components/CategoryView";

export const dynamic = "force-dynamic";
export const metadata = {
  title: "Epics",
  alternates: { canonical: "/epics" },
};

export default function Page() {
  return <CategoryView categoryKey="Epics" />;
}
