import { Navbar } from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowRight, FileText, Zap, Code, Upload, Scissors, Download } from "lucide-react";
import Link from "next/link";

export const metadata = { title: "Documentation | AutoClip AI", description: "Quick start guide and documentation for AutoClip AI." };

export default function DocsPage() {
    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-3xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-4">Documentation</h1>
                    <p className="text-muted-foreground text-lg mb-10">Everything you need to start creating viral clips.</p>

                    {/* Quick Start */}
                    <div className="mb-12">
                        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2"><Zap className="h-5 w-5 text-primary" /> Quick Start</h2>
                        <div className="space-y-4">
                            {[
                                { step: "1", title: "Create an Account", desc: "Register with your email, username, and password. You get 50 free credits.", icon: FileText },
                                { step: "2", title: "Paste a YouTube URL", desc: "Go to the dashboard and paste any YouTube video URL in the input field.", icon: Upload },
                                { step: "3", title: "AI Processes Your Video", desc: "Our AI analyzes the video, detects viral moments, applies face tracking and subtitles.", icon: Scissors },
                                { step: "4", title: "Download Your Clips", desc: "Download clips optimized for TikTok, Instagram Reels, YouTube Shorts, and Facebook.", icon: Download },
                            ].map((item) => (
                                <div key={item.step} className="flex gap-4 p-4 bg-card border border-border rounded-xl">
                                    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                                        <span className="text-primary font-bold">{item.step}</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-sm">{item.title}</h3>
                                        <p className="text-xs text-muted-foreground mt-1">{item.desc}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Features */}
                    <div className="mb-12">
                        <h2 className="text-2xl font-bold mb-6">Key Features</h2>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {[
                                { title: "Face Tracking", desc: "AI detects and follows speakers, keeping them centered in the frame" },
                                { title: "Hormozi-Style Subtitles", desc: "Animated captions with keyword highlighting for maximum engagement" },
                                { title: "Multi-Platform Export", desc: "Optimized for TikTok (9:16), Reels (9:16), Shorts (9:16), Facebook (1:1)" },
                                { title: "AI Viral Detection", desc: "Gemini and DeepSeek analyze content to find the most shareable moments" },
                                { title: "Social Auto-Post", desc: "Publish clips directly to TikTok and Instagram (Pro plan)" },
                                { title: "Bulk Processing", desc: "Process up to 10 videos simultaneously (Business plan)" },
                            ].map((f, i) => (
                                <Card key={i} className="bg-card border-border"><CardContent className="p-4"><h3 className="font-semibold text-sm mb-1">{f.title}</h3><p className="text-xs text-muted-foreground">{f.desc}</p></CardContent></Card>
                            ))}
                        </div>
                    </div>

                    {/* FAQ */}
                    <div>
                        <h2 className="text-2xl font-bold mb-6">FAQ</h2>
                        <div className="space-y-4">
                            {[
                                { q: "How many credits do I need per video?", a: "Each video costs 10 credits. Free accounts start with 50 credits (5 videos)." },
                                { q: "What video formats are supported?", a: "We support any public YouTube URL. The output is MP4 optimized for each platform." },
                                { q: "How long does processing take?", a: "Typically 3-5 minutes depending on video length and number of clips requested." },
                                { q: "Can I cancel my subscription?", a: "Yes, you can cancel anytime. Your access continues until the end of the billing period." },
                            ].map((item, i) => (
                                <div key={i} className="bg-card border border-border rounded-xl p-4">
                                    <h3 className="font-semibold text-sm mb-1">{item.q}</h3>
                                    <p className="text-xs text-muted-foreground">{item.a}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="text-center mt-12">
                        <Button asChild><Link href="/auth/register">Get Started <ArrowRight className="ml-2 h-4 w-4" /></Link></Button>
                    </div>
                </div>
            </section>
        </div>
    );
}
