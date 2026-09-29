import CategoryView from "@/components/CategoryView";

export const dynamic = "force-dynamic";
export const metadata = { title: "Bundles & Sets" };

export default function Page() {
  return <CategoryView categoryKey="Sets" />;
}
