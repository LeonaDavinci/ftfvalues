import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata = {
  metadataBase: new URL("https://www.ftfvalues.app"),
  title: {
    default:
      "FTF Values - Calculator - item value -  Flee the Facility Trading Value Guide & ",
    template: "%s - FTF Values",
  },
  description:
    "FTF Values - Flee the Facility trading value guide and item value calculator. Check FTF item values, stability tags and demand ratings for Legendary, Epic, Rare and Common items.",
  keywords: [
    "Flee the Facility",
    "FTF",
    "Roblox FTF",
    "FTF values",
    "FTF trading",
    "FTF item values",
  ],
  alternates: {
    canonical: "/",
  },
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "48x48" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
    ],
    apple: "/apple-touch-icon.png",
  },
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
