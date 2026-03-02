"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Scissors, ArrowRight, Play, Star, Users, Eye, Zap, ScanFace, Subtitles, Share2, Sparkles, FileVideo, BarChart3, Clock, DollarSign, CheckCircle2 } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Navbar } from "@/components/navbar";
import Link from "next/link";

/* ═══════════════════════════════════════════════════════
   HERO SECTION
   ═══════════════════════════════════════════════════════ */
function HeroSection() {
  return (
    <section className="relative overflow-hidden pt-20 pb-32">
      {/* Background Grid */}
      <div className="absolute inset-0 bg-grid opacity-30" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-primary/5 blur-3xl" />

      <div className="relative mx-auto max-w-4xl px-4 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-4 py-1.5 text-sm text-primary mb-8">
          <Sparkles className="h-4 w-4" />
          <span>AI-Powered Video Clipping Engine</span>
        </div>

        {/* Headline */}
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.1] mb-6">
          Turn Any Video Into{" "}
          <span className="text-gradient">Viral Clips</span>
        </h1>

        <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
          Paste a YouTube URL. Our AI finds the best moments, adds face tracking,
          dynamic subtitles, and exports optimized clips for TikTok, Reels & Shorts.
        </p>

        {/* Input-first CTA (inspired by autoclips) */}
        <div className="max-w-xl mx-auto">
          <div className="flex items-center gap-2 p-2 rounded-2xl bg-card border border-border shadow-2xl glow-green">
            <div className="flex items-center gap-2 flex-1 pl-4">
              <Play className="h-5 w-5 text-muted-foreground shrink-0" />
              <Input
                placeholder="Paste your YouTube URL here..."
                className="border-0 bg-transparent text-base focus-visible:ring-0 shadow-none placeholder:text-muted-foreground/60"
              />
            </div>
            <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90 font-semibold px-6 h-12 rounded-xl" asChild>
              <Link href="/dashboard">
                Clip Now <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-3 flex items-center justify-center gap-1">
            <CheckCircle2 className="h-3 w-3 text-primary" />
            Free to try — No credit card required
          </p>
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════
   SOCIAL PROOF COUNTERS
   ═══════════════════════════════════════════════════════ */
function SocialProof() {
  const stats = [
    { icon: FileVideo, value: "2,400+", label: "Clips Generated" },
    { icon: Users, value: "180+", label: "Beta Creators" },
    { icon: Eye, value: "12M+", label: "Views Generated" },
  ];
  return (
    <section className="py-16 border-y border-border/40">
      <div className="mx-auto max-w-5xl px-4 grid grid-cols-3 gap-8">
        {stats.map((s, i) => (
          <div key={i} className="text-center">
            <s.icon className="h-6 w-6 text-primary mx-auto mb-2" />
            <p className="text-3xl sm:text-4xl font-extrabold tracking-tight">{s.value}</p>
            <p className="text-sm text-muted-foreground mt-1">{s.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════
   FEATURES SECTION
   ═══════════════════════════════════════════════════════ */
function FeaturesSection() {
  const features = [
    {
      icon: ScanFace,
      title: "Smart Face Tracking",
      description: "MediaPipe-powered face detection keeps speakers perfectly centered, even in multi-person interviews.",
    },
    {
      icon: Subtitles,
      title: "Hormozi-Style Subtitles",
      description: "Dynamic word-by-word subtitles with semi-transparent background, proven to boost retention by 40%.",
    },
    {
      icon: Zap,
      title: "Multi-Engine AI Analysis",
      description: "Gemini, DeepSeek, Groq — our fallback system always finds the best viral moments, automatically.",
    },
    {
      icon: Share2,
      title: "Multi-Platform Export",
      description: "One click generates TikTok (9:16), Reels (9:16), and Facebook (4:5) versions with platform-specific color grading.",
    },
    {
      icon: BarChart3,
      title: "SEO-Ready Descriptions",
      description: "AI generates optimized titles, descriptions, and hashtags for each clip and each platform.",
    },
    {
      icon: Sparkles,
      title: "AI Effects Director",
      description: "Automatic zoom, transitions, hook flash, and audio normalization — driven by an AI-generated artistic plan.",
    },
  ];

  return (
    <section id="features" className="py-24 px-4">
      <div className="mx-auto max-w-6xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-4">
            Everything You Need to <span className="text-gradient">Go Viral</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto text-lg">
            From face tracking to SEO descriptions — our pipeline handles the entire workflow.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <Card key={i} className="bg-card border-border hover:border-primary/40 transition-colors group">
              <CardHeader>
                <div className="rounded-xl bg-primary/10 p-3 w-fit mb-3 group-hover:bg-primary/20 transition-colors">
                  <f.icon className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-lg">{f.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm leading-relaxed">{f.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════
   HOW IT WORKS
   ═══════════════════════════════════════════════════════ */
function HowItWorks() {
  const steps = [
    { step: "01", title: "Paste a URL", desc: "Drop any YouTube video link — podcasts, interviews, lectures, vlogs." },
    { step: "02", title: "AI Analyzes", desc: "Our multi-engine AI transcribes, identifies viral moments, and plans effects." },
    { step: "03", title: "Get Your Clips", desc: "Download ready-to-post clips for TikTok, Reels, and Facebook with SEO descriptions." },
  ];

  return (
    <section id="how-it-works" className="py-24 px-4 border-t border-border/40">
      <div className="mx-auto max-w-5xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-4">
            How It Works
          </h2>
          <p className="text-muted-foreground text-lg">Three steps. Zero editing skills required.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((s, i) => (
            <div key={i} className="relative text-center group">
              <div className="text-6xl font-black text-primary/10 mb-4 group-hover:text-primary/20 transition-colors">{s.step}</div>
              <h3 className="text-xl font-bold mb-2">{s.title}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">{s.desc}</p>
              {i < 2 && (
                <ArrowRight className="hidden md:block absolute top-8 -right-4 h-6 w-6 text-border" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════
   COMPARISON TABLE (DIY vs AutoClip)
   ═══════════════════════════════════════════════════════ */
function ComparisonSection() {
  return (
    <section className="py-24 px-4 border-t border-border/40">
      <div className="mx-auto max-w-5xl">
        <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-center mb-16">
          Why AutoClip <span className="text-gradient">Beats DIY</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* DIY */}
          <Card className="bg-card border-destructive/30">
            <CardHeader>
              <CardTitle className="text-destructive flex items-center gap-2">
                <Clock className="h-5 w-5" /> The Manual Approach
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              {[
                { item: "Watch & find moments manually", cost: "2-3 hrs" },
                { item: "Edit in Premiere / CapCut", cost: "1-2 hrs" },
                { item: "Add subtitles by hand", cost: "30 min" },
                { item: "Resize for each platform", cost: "30 min" },
                { item: "Write SEO descriptions", cost: "20 min" },
              ].map((r, i) => (
                <div key={i} className="flex justify-between items-center border-b border-border/40 pb-2">
                  <span className="text-muted-foreground">{r.item}</span>
                  <span className="font-medium text-destructive">{r.cost}</span>
                </div>
              ))}
              <div className="pt-2 flex justify-between font-bold text-base">
                <span>Total per video</span>
                <span className="text-destructive">4-6 hours</span>
              </div>
            </CardContent>
          </Card>

          {/* AutoClip */}
          <Card className="bg-card border-primary/40 glow-green">
            <CardHeader>
              <CardTitle className="text-primary flex items-center gap-2">
                <Zap className="h-5 w-5" /> The AutoClip Way
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              {[
                { item: "AI finds viral moments", cost: "Auto" },
                { item: "Face tracking + effects", cost: "Auto" },
                { item: "Hormozi-style subtitles", cost: "Auto" },
                { item: "Multi-platform export", cost: "Auto" },
                { item: "SEO titles & hashtags", cost: "Auto" },
              ].map((r, i) => (
                <div key={i} className="flex justify-between items-center border-b border-border/40 pb-2">
                  <span className="text-muted-foreground">{r.item}</span>
                  <span className="font-medium text-primary">{r.cost}</span>
                </div>
              ))}
              <div className="pt-2 flex justify-between font-bold text-base">
                <span>Total per video</span>
                <span className="text-primary">~5 minutes</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════
   PRICING SECTION
   ═══════════════════════════════════════════════════════ */
function PricingSection() {
  const plans = [
    { name: "Starter", price: "Free", period: "", credits: "3 clips/month", features: ["1-min clips", "Basic subtitles", "YouTube export", "Gemini AI"], cta: "Get Started", highlight: false },
    { name: "Pro", price: "$29", period: "/mo", credits: "50 clips/month", features: ["5-min clips", "Face tracking", "Multi-platform", "All AI engines", "SEO descriptions"], cta: "Go Pro", highlight: true },
    { name: "Business", price: "$79", period: "/mo", credits: "200 clips/month", features: ["10-min clips", "Priority rendering", "API access", "Custom branding", "Dedicated support"], cta: "Contact Sales", highlight: false },
  ];

  return (
    <section id="pricing" className="py-24 px-4 border-t border-border/40">
      <div className="mx-auto max-w-5xl">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-4 py-1.5 text-sm text-primary mb-6">
            <DollarSign className="h-4 w-4" />
            Simple, transparent pricing
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-4">
            Choose Your <span className="text-gradient">Plan</span>
          </h2>
          <p className="text-muted-foreground text-lg">Start free. Upgrade when you need more power.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((p, i) => (
            <Card key={i} className={`bg-card relative ${p.highlight ? 'border-primary glow-green' : 'border-border'}`}>
              {p.highlight && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-primary text-primary-foreground text-xs font-bold px-4 py-1">
                  Most Popular
                </div>
              )}
              <CardHeader className="text-center pb-2">
                <CardTitle className="text-xl">{p.name}</CardTitle>
                <div className="mt-4">
                  <span className="text-4xl font-extrabold">{p.price}</span>
                  <span className="text-muted-foreground text-sm">{p.period}</span>
                </div>
                <p className="text-xs text-primary font-medium mt-2">{p.credits}</p>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-2.5 text-sm">
                  {p.features.map((f, j) => (
                    <li key={j} className="flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-primary shrink-0" />
                      <span className="text-muted-foreground">{f}</span>
                    </li>
                  ))}
                </ul>
                <Button className={`w-full ${p.highlight ? 'bg-primary text-primary-foreground hover:bg-primary/90' : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'}`} asChild>
                  <Link href="/dashboard">{p.cta}</Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        <p className="text-center text-xs text-muted-foreground mt-8 flex items-center justify-center gap-1">
          🔒 Secure payment powered by Stripe · Cancel anytime
        </p>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════════════════ */
function Footer() {
  return (
    <footer className="border-t border-border/40 py-12 px-4">
      <div className="mx-auto max-w-6xl grid grid-cols-2 md:grid-cols-4 gap-8 text-sm">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Scissors className="h-5 w-5 text-primary" />
            <span className="font-bold">AutoClipAI</span>
          </div>
          <p className="text-muted-foreground text-xs leading-relaxed">
            Transform any YouTube video into viral clips with AI-powered face tracking, subtitles, and multi-platform export.
          </p>
        </div>
        {[
          { title: "Product", links: ["Features", "Pricing", "Roadmap", "Changelog"] },
          { title: "Resources", links: ["Documentation", "API Reference", "Blog", "Guides"] },
          { title: "Company", links: ["About", "Contact", "Privacy", "Terms"] },
        ].map((col, i) => (
          <div key={i}>
            <h4 className="font-semibold mb-3">{col.title}</h4>
            <ul className="space-y-2 text-muted-foreground">
              {col.links.map((l, j) => (
                <li key={j}>
                  <Link href="#" className="hover:text-foreground transition-colors">{l}</Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="mx-auto max-w-6xl mt-10 pt-6 border-t border-border/30 text-center text-xs text-muted-foreground">
        © 2026 AutoClip AI. All rights reserved.
      </div>
    </footer>
  );
}

/* ═══════════════════════════════════════════════════════
   MAIN PAGE
   ═══════════════════════════════════════════════════════ */
export default function Home() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <HeroSection />
      <SocialProof />
      <FeaturesSection />
      <HowItWorks />
      <ComparisonSection />
      <PricingSection />
      <Footer />
    </div>
  );
}
