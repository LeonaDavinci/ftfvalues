import CategoryView from "@/components/CategoryView";

export const dynamic = "force-dynamic";
export const metadata = { title: "Legendaries" };

export default function Page() {
  return <CategoryView categoryKey="Legendaries" />;
}
