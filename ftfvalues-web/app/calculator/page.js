import Calculator from "@/components/Calculator";
import { getAllItems, getLastUpdated } from "@/lib/data";

export const dynamic = "force-dynamic";

export const metadata = {
  title: "FTF Calculator",
  description:
    "FTF trade calculator — build both sides of a trade, compare totals in fv, and see instantly if you Win, Lose, or make a Fair trade.",
};

export default function CalculatorPage() {
  const items = getAllItems();
  const lastUpdated = getLastUpdated();
  return (
    <>
      <section className="calc-hero">
        <h1>🧮 FTF Calculator</h1>
        <p>
          Pick items for both sides of your trade — totals and a Win / Fair /
          Lose verdict update instantly as you build the offer.
        </p>
      </section>
      <Calculator items={items} lastUpdated={lastUpdated} />
    </>
  );
}
