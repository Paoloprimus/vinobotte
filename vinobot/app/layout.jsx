import { Literata } from "next/font/google";
import "./globals.css";

const literata = Literata({ subsets: ["latin"], display: "swap", variable: "--font-testo" });

export const metadata = {
  title: "VinoBotte",
  description: "Come le intelligenze artificiali vedono la sua cantina.",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }) {
  return (
    <html lang="it" className={literata.variable}>
      <body>{children}</body>
    </html>
  );
}
