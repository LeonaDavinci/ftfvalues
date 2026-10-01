import CategoryView from "@/components/CategoryView";

export const dynamic = "force-dynamic";
export const metadata = {
  title: "Rares",
  alternates: { canonical: "/rares" },
};

export default function Page() {
  return <CategoryView categoryKey="Rares" />;
}
