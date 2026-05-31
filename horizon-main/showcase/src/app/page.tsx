import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import ArchitectureSection from "@/components/ArchitectureSection";
import DemoSection from "@/components/DemoSection";
import IntegrationsSection from "@/components/IntegrationsSection";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="flex-1 flex flex-col">
      <Navbar />
      <HeroSection />
      <ArchitectureSection />
      <DemoSection />
      <IntegrationsSection />
      <Footer />
    </main>
  );
}
