import CategoryView from "@/components/CategoryView";

export const dynamic = "force-dynamic";
export const metadata = {
  title: "Legendaries",
  alternates: { canonical: "/legendaries" },
};

export default function Page() {
  return <CategoryView categoryKey="Legendaries" />;
}
