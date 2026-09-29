import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata = {
  title: {
    default: "FTF Values - Flee the Facility Trading Value Guide",
    template: "%s - FTF Values",
  },
  description:
    "The ultimate Flee the Facility value guide. Check item values, stability tags, and demand ratings for Legendary, Epic, Rare and Common items. Updated daily.",
  keywords: [
    "Flee the Facility",
    "FTF",
    "Roblox FTF",
    "FTF values",
    "FTF trading",
    "FTF item values",
  ],
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
