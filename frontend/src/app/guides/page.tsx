import { Navbar } from "@/components/navbar";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BookOpen, Play, ArrowRight, Video, Scissors, Share2, BarChart3, Zap, Users } from "lucide-react";
import Link from "next/link";

export const metadata = { title: "Guides | AutoClip AI", description: "Step-by-step guides and tutorials for AutoClip AI." };

export default function GuidesPage() {
    const guides = [
        {
            icon: Video,
            title: "Creating Your First Clip",
            desc: "Learn the basics: paste a URL, configure settings, and download your first viral clip in under 5 minutes.",
            difficulty: "Beginner",
            time: "5 min",
        },
        {
            icon: Scissors,
            title: "Mastering Face Tracking",
            desc: "How our AI face tracking works and tips for getting the best results with multi-speaker videos.",
            difficulty: "Intermediate",
            time: "8 min",
        },
        {
            icon: Play,
            title: "Hormozi-Style Subtitles Guide",
            desc: "Learn how to create eye-catching animated subtitles that boost viewer retention and engagement.",
            difficulty: "Beginner",
            time: "6 min",
        },
        {
            icon: Share2,
            title: "Multi-Platform Export Strategy",
            desc: "Optimize your clips for TikTok, Instagram Reels, YouTube Shorts, and Facebook for maximum reach.",
            difficulty: "Intermediate",
            time: "10 min",
        },
        {
            icon: Zap,
            title: "Automating Your Content Pipeline",
            desc: "Set up automated workflows to clip, subtitle, and publish content with minimal manual effort.",
            difficulty: "Advanced",
            time: "15 min",
        },
        {
            icon: BarChart3,
            title: "Using Analytics to Grow",
            desc: "Understand your clip performance data and use insights to create more viral content.",
            difficulty: "Intermediate",
            time: "8 min",
        },
        {
            icon: Users,
            title: "Team Collaboration Setup",
            desc: "Set up team accounts, manage permissions, and collaborate on content creation.",
            difficulty: "Advanced",
            time: "10 min",
        },
        {
            icon: BookOpen,
            title: "API Integration Guide",
            desc: "Connect AutoClip AI to your existing tools and workflows using our REST API.",
            difficulty: "Advanced",
            time: "20 min",
        },
    ];

    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-4xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-4 flex items-center gap-3">
                        <BookOpen className="h-8 w-8 text-primary" /> Guides & Tutorials
                    </h1>
                    <p className="text-muted-foreground text-lg mb-10">Step-by-step guides to help you get the most out of AutoClip AI.</p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {guides.map((guide, i) => (
                            <Card key={i} className="bg-card border-border hover:border-primary/50 transition-all group">
                                <CardContent className="p-6">
                                    <div className="flex items-start gap-4">
                                        <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                                            <guide.icon className="h-5 w-5 text-primary" />
                                        </div>
                                        <div className="flex-1">
                                            <h3 className="font-semibold mb-1 group-hover:text-primary transition-colors">{guide.title}</h3>
                                            <p className="text-xs text-muted-foreground mb-3">{guide.desc}</p>
                                            <div className="flex items-center gap-3">
                                                <span className={`text-xs px-2 py-0.5 rounded-full ${guide.difficulty === "Beginner" ? "bg-green-500/10 text-green-400" : guide.difficulty === "Intermediate" ? "bg-blue-500/10 text-blue-400" : "bg-purple-500/10 text-purple-400"}`}>
                                                    {guide.difficulty}
                                                </span>
                                                <span className="text-xs text-muted-foreground">{guide.time} read</span>
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    <div className="text-center mt-12">
                        <Button asChild><Link href="/docs">View Full Documentation <ArrowRight className="ml-2 h-4 w-4" /></Link></Button>
                    </div>
                </div>
            </section>
        </div>
    );
}
