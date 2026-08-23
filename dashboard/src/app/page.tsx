export const dynamic = "force-dynamic";
import { Hero } from "@/components/landing/Hero";
import { SourceMarquee } from "@/components/landing/SourceMarquee";
import { StatsBar } from "@/components/landing/StatsBar";
import { BentoFeatures } from "@/components/landing/BentoFeatures";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { ModuleShowcase } from "@/components/landing/ModuleShowcase";
import { SelfHealSection } from "@/components/landing/SelfHealSection";
import { TechSection } from "@/components/landing/TechSection";
import { FinalCTA } from "@/components/landing/FinalCTA";
import { Footer } from "@/components/landing/Footer";
import { fetchOverview, fetchHealEvents } from "@/lib/api";

export default async function LandingPage() {
  let overview = null;
  let heals: unknown[] = [];
  try {
    [overview, heals] = await Promise.all([fetchOverview(), fetchHealEvents()]);
  } catch {
    // backend offline — landing still renders with fallback copy
  }

  return (
    <div className="bg-background min-h-screen grid-bg">
      <Hero />
      <SourceMarquee />
      <StatsBar overview={overview} />
      <BentoFeatures />
      <HowItWorks />
      <ModuleShowcase overview={overview} />
      <SelfHealSection heals={heals} />
      <TechSection />
      <FinalCTA />
      <Footer />
    </div>
  );
}
