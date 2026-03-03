import { Navbar } from "@/components/navbar";
import { Card, CardContent } from "@/components/ui/card";
import { Rocket, CheckCircle2, Clock, Sparkles } from "lucide-react";

export const metadata = { title: "Roadmap | AutoClip AI", description: "See what's coming next for AutoClip AI." };

export default function RoadmapPage() {
    const phases = [
        {
            quarter: "Q1 2026",
            status: "completed",
            items: [
                "AI-powered viral moment detection (Gemini & DeepSeek)",
                "Face tracking with speaker-centered framing",
                "Hormozi-style animated subtitles",
                "Multi-platform export (TikTok, Reels, Shorts, Facebook)",
                "User dashboard with job management",
                "Credit-based billing system",
            ],
        },
        {
            quarter: "Q2 2026",
            status: "in-progress",
            items: [
                "Social media auto-posting (TikTok, Instagram, YouTube)",
                "Scheduled posting with optimal timing",
                "Analytics dashboard with engagement metrics",
                "Bulk video processing (up to 10 simultaneous)",
                "Custom branding & watermarks",
                "Team collaboration features",
            ],
        },
        {
            quarter: "Q3 2026",
            status: "planned",
            items: [
                "White-label solution for agencies",
                "AI thumbnail generation",
                "Multi-language subtitle support (20+ languages)",
                "Advanced analytics with revenue tracking",
                "Webhook integrations",
                "Mobile app (iOS & Android)",
            ],
        },
        {
            quarter: "Q4 2026",
            status: "planned",
            items: [
                "AI script-to-video generation",
                "Custom AI voice synthesis",
                "Real-time collaboration editing",
                "Enterprise SSO & SAML",
                "Advanced API with webhook callbacks",
                "Content calendar with AI recommendations",
            ],
        },
    ];

    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-3xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-4 flex items-center gap-3">
                        <Rocket className="h-8 w-8 text-primary" /> Roadmap
                    </h1>
                    <p className="text-muted-foreground text-lg mb-10">Our vision for AutoClip AI — what we&apos;ve built and what&apos;s coming.</p>

                    <div className="space-y-6">
                        {phases.map((phase, i) => (
                            <Card key={i} className={`bg-card border-border ${phase.status === "in-progress" ? "border-primary/50 glow-green" : ""}`}>
                                <CardContent className="p-6">
                                    <div className="flex items-center gap-3 mb-4">
                                        <span className="text-lg font-bold">{phase.quarter}</span>
                                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${phase.status === "completed" ? "bg-green-500/10 text-green-400" : phase.status === "in-progress" ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground"}`}>
                                            {phase.status === "completed" ? "✅ Completed" : phase.status === "in-progress" ? "🚧 In Progress" : "📋 Planned"}
                                        </span>
                                    </div>
                                    <ul className="space-y-2">
                                        {phase.items.map((item, j) => (
                                            <li key={j} className="flex items-center gap-2 text-sm">
                                                {phase.status === "completed" ? (
                                                    <CheckCircle2 className="h-4 w-4 text-green-400 shrink-0" />
                                                ) : phase.status === "in-progress" ? (
                                                    <Clock className="h-4 w-4 text-primary shrink-0" />
                                                ) : (
                                                    <Sparkles className="h-4 w-4 text-muted-foreground shrink-0" />
                                                )}
                                                <span className="text-muted-foreground">{item}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
}
