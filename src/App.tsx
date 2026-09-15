import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { TrustCarousel } from "./components/TrustCarousel";
import { TechShowcase } from "./components/TechShowcase";
import { Timeline } from "./components/Timeline";
import { PartesForm } from "./components/PartesForm";
import { ContactMap } from "./components/ContactMap";
import { Footer } from "./components/Footer";

export default function App() {
  return (
    <div className="bg-titanium-950">
      <Navbar />
      <main>
        <Hero />
        <TrustCarousel />
        <TechShowcase />
        <Timeline />
        <PartesForm />
        <ContactMap />
      </main>
      <Footer />
    </div>
  );
}
