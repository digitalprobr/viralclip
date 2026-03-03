import { Navbar } from "@/components/navbar";
import { Sparkles, Zap, Globe, Shield, Users, Code } from "lucide-react";
import Link from "next/link";

export const metadata = { title: "About | AutoClip AI", description: "Learn about AutoClip AI — our mission, technology, and the team behind the AI video clipping platform." };

export default function AboutPage() {
    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-3xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-6">About <span className="text-gradient">AutoClip AI</span></h1>

                    <div className="space-y-8 text-muted-foreground leading-relaxed">
                        <div>
                            <h2 className="text-xl font-bold text-foreground mb-3">Our Mission</h2>
                            <p>AutoClip AI empowers content creators to transform any video into viral short-form clips using artificial intelligence. We believe that great content deserves to be seen — and AI can help it reach millions.</p>
                        </div>

                        <div>
                            <h2 className="text-xl font-bold text-foreground mb-3">What We Do</h2>
                            <p>Our platform analyzes videos to find the most engaging moments, applies AI-powered face tracking and dynamic subtitles, and exports clips optimized for TikTok, Instagram Reels, YouTube Shorts, and Facebook. What used to take hours of manual editing now takes minutes.</p>
                        </div>

                        <div>
                            <h2 className="text-xl font-bold text-foreground mb-4">Our Technology</h2>
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                {[
                                    { icon: Sparkles, title: "AI Analysis", desc: "Gemini & DeepSeek for viral moment detection" },
                                    { icon: Zap, title: "Face Tracking", desc: "Computer vision for speaker-centered framing" },
                                    { icon: Globe, title: "Multi-Platform", desc: "Optimized for TikTok, Reels, Shorts & Facebook" },
                                    { icon: Shield, title: "Secure", desc: "End-to-end encryption, GDPR compliant" },
                                    { icon: Users, title: "50K+ Creators", desc: "Trusted by content creators worldwide" },
                                    { icon: Code, title: "Open API", desc: "RESTful API for enterprise integration" },
                                ].map((item, i) => (
                                    <div key={i} className="bg-card border border-border rounded-xl p-4">
                                        <item.icon className="h-5 w-5 text-primary mb-2" />
                                        <h3 className="font-semibold text-foreground text-sm">{item.title}</h3>
                                        <p className="text-xs text-muted-foreground">{item.desc}</p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div>
                            <h2 className="text-xl font-bold text-foreground mb-3">Founded</h2>
                            <p>AutoClip AI was founded in 2025 with a simple idea: make professional video editing accessible to everyone through AI. Built by a team of AI engineers, video professionals, and growth marketers, we&apos;re on a mission to democratize video content creation.</p>
                        </div>

                        <div className="text-center pt-8 border-t border-border/50">
                            <p className="text-sm">Questions? <Link href="/contact" className="text-primary hover:underline">Contact us</Link></p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
