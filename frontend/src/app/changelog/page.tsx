import { Navbar } from "@/components/navbar";
import { Card, CardContent } from "@/components/ui/card";
import { GitBranch, Plus, Bug, Zap } from "lucide-react";

export const metadata = { title: "Changelog | AutoClip AI", description: "AutoClip AI changelog — see all updates and improvements." };

export default function ChangelogPage() {
    const releases = [
        {
            version: "2.1.0",
            date: "March 1, 2026",
            tag: "Latest",
            changes: [
                { type: "feature", text: "Username/password registration with robust password validation" },
                { type: "feature", text: "Blog section with 20+ SEO articles on AI video creation" },
                { type: "feature", text: "All footer pages now functional (About, Contact, Privacy, Terms, etc.)" },
                { type: "feature", text: "Enhanced pricing with social auto-post and scheduled posting" },
                { type: "improvement", text: "Updated API reference documentation" },
            ],
        },
        {
            version: "2.0.0",
            date: "February 28, 2026",
            tag: null,
            changes: [
                { type: "feature", text: "Complete SaaS platform launch with Dockerized architecture" },
                { type: "feature", text: "AI-powered viral moment detection using Gemini & DeepSeek" },
                { type: "feature", text: "Advanced face tracking with speaker-centered framing" },
                { type: "feature", text: "Hormozi-style animated subtitles with keyword highlighting" },
                { type: "feature", text: "Multi-platform export (TikTok, Instagram Reels, YouTube Shorts)" },
                { type: "feature", text: "Credit-based billing with 50 free credits on signup" },
                { type: "feature", text: "Real-time job progress with SSE streaming" },
            ],
        },
        {
            version: "1.5.0",
            date: "February 15, 2026",
            tag: null,
            changes: [
                { type: "feature", text: "GitHub repository setup with CI/CD pipeline" },
                { type: "improvement", text: "Worker/API separation for better scalability" },
                { type: "bugfix", text: "Fixed worker database update failures" },
                { type: "bugfix", text: "Fixed clip file URL construction (double prefix issue)" },
            ],
        },
        {
            version: "1.0.0",
            date: "February 1, 2026",
            tag: null,
            changes: [
                { type: "feature", text: "Initial release — core clipping engine" },
                { type: "feature", text: "YouTube video downloading and transcription" },
                { type: "feature", text: "Basic subtitle generation" },
                { type: "feature", text: "Single-platform export" },
            ],
        },
    ];

    function getIcon(type: string) {
        switch (type) {
            case "feature": return <Plus className="h-3.5 w-3.5 text-green-400 shrink-0" />;
            case "improvement": return <Zap className="h-3.5 w-3.5 text-primary shrink-0" />;
            case "bugfix": return <Bug className="h-3.5 w-3.5 text-orange-400 shrink-0" />;
            default: return <GitBranch className="h-3.5 w-3.5 text-muted-foreground shrink-0" />;
        }
    }

    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-3xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-4 flex items-center gap-3">
                        <GitBranch className="h-8 w-8 text-primary" /> Changelog
                    </h1>
                    <p className="text-muted-foreground text-lg mb-10">All updates, features, and fixes.</p>

                    <div className="space-y-6">
                        {releases.map((release, i) => (
                            <Card key={i} className={`bg-card border-border ${i === 0 ? "border-primary/30" : ""}`}>
                                <CardContent className="p-6">
                                    <div className="flex items-center gap-3 mb-4">
                                        <span className="text-xl font-bold">v{release.version}</span>
                                        <span className="text-xs text-muted-foreground">{release.date}</span>
                                        {release.tag && (
                                            <span className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded-full font-medium">{release.tag}</span>
                                        )}
                                    </div>
                                    <ul className="space-y-2">
                                        {release.changes.map((change, j) => (
                                            <li key={j} className="flex items-start gap-2 text-sm text-muted-foreground">
                                                {getIcon(change.type)}
                                                <span>{change.text}</span>
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
