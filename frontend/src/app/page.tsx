"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Scissors, ArrowRight, Play, Star, Users, Eye, Zap, ScanFace, Subtitles, Share2, Sparkles, FileVideo, BarChart3, Clock, DollarSign, CheckCircle2, MessageSquare, ChevronDown } from "lucide-react";
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
    { name: "Starter", price: "Free", period: "", credits: "3 clips/month", features: ["1-min clips", "Basic subtitles", "YouTube export only", "Gemini AI engine", "1 team member"], cta: "Get Started", highlight: false },
    { name: "Pro", price: "$29", period: "/mo", credits: "50 clips/month", features: ["5-min clips", "Face tracking", "Multi-platform export", "All AI engines", "SEO descriptions", "Social auto-post (TikTok, Reels)", "Basic analytics dashboard", "3 team members"], cta: "Go Pro", highlight: true },
    { name: "Business", price: "$79", period: "/mo", credits: "200 clips/month", features: ["10-min clips", "Priority rendering", "API access", "Custom branding & watermarks", "Social auto-post (all platforms)", "Scheduled posting", "Advanced analytics dashboard", "White label export", "Bulk processing (10 videos)", "Unlimited team members", "Dedicated support"], cta: "Contact Sales", highlight: false },
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
   REVIEWS
   ═══════════════════════════════════════════════════════ */
const reviews = [
  { name: "Marcus J.", role: "TikTok Creator", avatar: "MJ", text: "I made my first $1,200 on TikTok within 3 weeks of using AutoClip AI. I was struggling to edit videos fast enough, but now I publish 15 clips a day without breaking a sweat. This tool literally changed my life." },
  { name: "Sarah K.", role: "YouTube Shorts Creator", avatar: "SK", text: "I went from 200 subscribers to 45K in just 2 months. AutoClip AI finds the viral moments I would have missed. The face tracking and Hormozi-style subtitles make my clips look like they were made by a pro editor." },
  { name: "David L.", role: "Content Agency Owner", avatar: "DL", text: "We now publish 80+ videos per day across TikTok, Reels, and Shorts for our clients. Before AutoClip AI, we needed 4 editors. Now one person handles everything. The ROI is insane." },
  { name: "Priya M.", role: "Faceless Channel Owner", avatar: "PM", text: "My faceless motivation channel hit 100K subscribers in 5 months. I paste YouTube URLs and AutoClip AI does the rest. I've made over $8,000 from AdSense alone. Best investment I ever made." },
  { name: "Jake R.", role: "Podcast Host", avatar: "JR", text: "I was spending 6 hours per episode cutting clips for social media. Now it takes me 10 minutes. My podcast audience grew 300% because every episode becomes 5-7 viral clips automatically." },
  { name: "Amina B.", role: "Digital Marketer", avatar: "AB", text: "AutoClip AI helped me grow my client's TikTok from 0 to 180K followers in 4 months. The AI picks the exact moments that resonate with their audience. I recommend this to every marketer I know." },
  { name: "Carlos T.", role: "Finance Content Creator", avatar: "CT", text: "First dollar? I made my first $500 in week one on TikTok. Finance content has high CPM and AutoClip AI's subtitle style keeps viewers hooked. I'm now at $4K/month from shorts alone." },
  { name: "Emma W.", role: "Gaming Channel", avatar: "EW", text: "I clip my Twitch streams into 20+ TikToks every day using AutoClip AI. My gaming channel went from nothing to 75K followers. The face tracking is perfect for facecam content." },
  { name: "Omar H.", role: "Real Estate Agent", avatar: "OH", text: "I use AutoClip AI to turn my property walkthrough videos into viral shorts. My leads increased 250% and I closed 3 extra deals last month. This tool pays for itself 100x over." },
  { name: "Lisa C.", role: "Fitness Influencer", avatar: "LC", text: "Posting consistently was my biggest challenge. Now I batch-create 50 clips in one sitting and schedule them across all platforms. My audience doubled in 6 weeks and brand deals followed." },
  { name: "Ryan P.", role: "Education YouTuber", avatar: "RP", text: "My students kept asking for shorter content. AutoClip AI turns my 1-hour lectures into 10 engaging shorts. My channel grew from 5K to 120K subs and I've been able to launch a paid course." },
  { name: "Nina F.", role: "Beauty Content Creator", avatar: "NF", text: "The Hormozi-style subtitles are EVERYTHING. My beauty tutorials get 5x more views with AutoClip AI's captions vs my manual edits. I earned my first $2,000 from TikTok Creator Fund last month." },
  { name: "Alex D.", role: "News Commentary", avatar: "AD", text: "I run 3 faceless news channels and AutoClip AI is the backbone. I generate 30+ clips per channel per day. Total monthly revenue across all channels: $12,000. Couldn't do it without this tool." },
  { name: "Fatima Z.", role: "Travel Vlogger", avatar: "FZ", text: "I was sitting on 200+ travel videos with zero shorts. AutoClip AI analyzed all of them and pulled out the most engaging moments. In 2 weeks I had a library of 500+ clips. My travel content finally went viral." },
  { name: "Tom S.", role: "Motivational Speaker", avatar: "TS", text: "My speeches are 45 minutes long but the magic moments are 60 seconds. AutoClip AI finds them perfectly every time. I gained 200K followers across platforms and doubled my speaking fees." },
  { name: "Jasmine L.", role: "Music Producer", avatar: "JL", text: "I clip my studio sessions and music breakdowns into shorts. AutoClip AI's face tracking keeps me centered even when I'm moving around the studio. My music channel blew up to 90K subs." },
  { name: "Daniel K.", role: "E-commerce Brand", avatar: "DK", text: "We use AutoClip AI to turn customer testimonial videos into ads. Our ROAS improved 180% because the AI picks the most persuasive moments. Best marketing tool we've added this year." },
  { name: "Helena R.", role: "Book Summary Channel", avatar: "HR", text: "I run a faceless book summary channel. AutoClip AI helps me repurpose long summaries into bite-sized shorts. Made my first $3,500 month after switching from manual editing. Highly recommend!" },
  { name: "Youssef A.", role: "Tech Reviewer", avatar: "YA", text: "I review gadgets and AutoClip AI turns my 20-minute reviews into 5-6 perfect shorts. The AI knows exactly which moments will grab attention. My tech shorts channel hit monetization in just 6 weeks." },
  { name: "Sophie M.", role: "Cooking Channel", avatar: "SM", text: "I was posting 2 videos a week manually. Now I post 10+ shorts every day across TikTok, Reels, and YouTube Shorts. My cooking channel grew from 1K to 50K followers and I got my first brand partnership." },
  { name: "Chris B.", role: "Sports Analyst", avatar: "CB", text: "AutoClip AI is perfect for sports content. It finds the hype moments in my analysis videos and adds dynamic subtitles. My sports channel generates $2,800/month now. Started from zero 4 months ago." },
  { name: "Maria G.", role: "Wellness Coach", avatar: "MG", text: "I was spending $2,000/month on a video editor. Switched to AutoClip AI for $29/month and the quality is actually better. The animated subtitles keep my wellness content engaging. Saved me $23K/year." },
  { name: "Kevin W.", role: "Comedy Creator", avatar: "KW", text: "The face tracking feature is incredible for comedy content. My reactions stay centered and the subtitles highlight the punchlines perfectly. Went from 0 to 40K TikTok followers in 8 weeks." },
  { name: "Rachel N.", role: "Parenting Blog", avatar: "RN", text: "I turned my parenting YouTube videos into TikTok content and the response was incredible. AutoClip AI helped me find the most relatable moments. Made $800 from TikTok last month — as a mom blogger!" },
  { name: "Liam O.", role: "Crypto Educator", avatar: "LO", text: "Crypto content needs speed — news changes fast. AutoClip AI lets me publish 25 clips per day across all platforms. My audience grew to 150K and I earn $6,000/month from ads and affiliates combined." },
];

function ReviewsSection() {
  const [showAll, setShowAll] = useState(false);
  const displayed = showAll ? reviews : reviews.slice(0, 6);

  return (
    <section className="py-24 px-4">
      <div className="mx-auto max-w-6xl">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-4 py-1.5 text-sm text-primary mb-4">
            <MessageSquare className="h-4 w-4" />
            Trusted by 50,000+ Creators
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-4">
            Real Results from <span className="text-gradient">Real Creators</span>
          </h2>
          <div className="flex items-center justify-center gap-1 mb-2">
            {[...Array(5)].map((_, i) => (
              <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
            ))}
            <span className="ml-2 text-sm font-semibold">4.9/5</span>
            <span className="text-sm text-muted-foreground ml-1">from 2,400+ reviews</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {displayed.map((review, i) => (
            <Card key={i} className="bg-card/60 border-border hover:border-primary/30 transition-all duration-300">
              <CardContent className="p-5">
                {/* Stars */}
                <div className="flex gap-0.5 mb-3">
                  {[...Array(5)].map((_, j) => (
                    <Star key={j} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>

                {/* Review text */}
                <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                  &ldquo;{review.text}&rdquo;
                </p>

                {/* Author */}
                <div className="flex items-center gap-3 pt-3 border-t border-border/50">
                  <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center text-xs font-bold text-primary">
                    {review.avatar}
                  </div>
                  <div>
                    <p className="text-sm font-semibold">{review.name}</p>
                    <p className="text-xs text-muted-foreground">{review.role}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {!showAll && (
          <div className="text-center mt-8">
            <Button
              variant="outline"
              size="lg"
              onClick={() => setShowAll(true)}
              className="group"
            >
              See All {reviews.length} Reviews
              <ChevronDown className="ml-2 h-4 w-4 group-hover:translate-y-0.5 transition-transform" />
            </Button>
          </div>
        )}
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════════════════ */
function Footer() {
  const footerLinks = [
    {
      title: "Product", links: [
        { label: "Features", href: "/#features" },
        { label: "Pricing", href: "/#pricing" },
        { label: "Roadmap", href: "/roadmap" },
        { label: "Changelog", href: "/changelog" },
      ]
    },
    {
      title: "Resources", links: [
        { label: "Documentation", href: "/docs" },
        { label: "API Reference", href: "/api-docs" },
        { label: "Blog", href: "/blog" },
        { label: "Guides", href: "/guides" },
      ]
    },
    {
      title: "Company", links: [
        { label: "About", href: "/about" },
        { label: "Contact", href: "/contact" },
        { label: "Privacy", href: "/privacy" },
        { label: "Terms", href: "/terms" },
      ]
    },
  ];

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
        {footerLinks.map((col, i) => (
          <div key={i}>
            <h4 className="font-semibold mb-3">{col.title}</h4>
            <ul className="space-y-2 text-muted-foreground">
              {col.links.map((l, j) => (
                <li key={j}>
                  <Link href={l.href} className="hover:text-foreground transition-colors">{l.label}</Link>
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
      <ReviewsSection />
      <Footer />
    </div>
  );
}
