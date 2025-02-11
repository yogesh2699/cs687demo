import "./globals.css";

export const metadata = {
  title: "Medical Clinic Chatbot",
  description: "A chatbot for the medical clinic.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}