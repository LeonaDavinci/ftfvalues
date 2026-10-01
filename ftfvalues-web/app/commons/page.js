import CategoryView from "@/components/CategoryView";

export const dynamic = "force-dynamic";
export const metadata = {
  title: "Commons",
  alternates: { canonical: "/commons" },
};

export default function Page() {
  return <CategoryView categoryKey="Commons" />;
}
