import { Navbar } from "@/components/navbar";
import { Card, CardContent } from "@/components/ui/card";
import { Code, ArrowRight } from "lucide-react";
import Link from "next/link";

export const metadata = { title: "API Reference | AutoClip AI", description: "AutoClip AI API documentation — endpoints, authentication, and examples." };

export default function ApiDocsPage() {
    const endpoints = [
        { method: "POST", path: "/api/v1/auth/signup", desc: "Register a new user", body: '{ "username": "string", "email": "string", "password": "string", "confirm_password": "string" }' },
        { method: "POST", path: "/api/v1/auth/login", desc: "Login with email and password", body: '{ "email": "string", "password": "string" }' },
        { method: "GET", path: "/api/v1/auth/me", desc: "Get authenticated user profile", body: null },
        { method: "POST", path: "/api/v1/auth/logout", desc: "Clear session", body: null },
        { method: "POST", path: "/api/v1/clip", desc: "Submit a new clip job", body: '{ "url": "youtube_url", "preferred_engine": "auto", "num_clips": 3 }' },
        { method: "GET", path: "/api/v1/jobs", desc: "List all jobs for current user", body: null },
        { method: "GET", path: "/api/v1/tasks/{task_id}", desc: "Get task status", body: null },
        { method: "GET", path: "/api/v1/tasks/{task_id}/stream", desc: "SSE stream for progress updates", body: null },
        { method: "GET", path: "/api/v1/clips/{job_id}/files", desc: "List generated clip files", body: null },
        { method: "GET", path: "/health", desc: "Health check", body: null },
    ];

    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-4xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-4 flex items-center gap-3">
                        <Code className="h-8 w-8 text-primary" /> API Reference
                    </h1>
                    <p className="text-muted-foreground text-lg mb-6">RESTful API for integrating AutoClip AI into your workflow.</p>

                    <div className="bg-card border border-border rounded-xl p-4 mb-10">
                        <h3 className="font-semibold text-sm mb-2">Base URL</h3>
                        <code className="text-primary text-sm bg-primary/5 px-3 py-1 rounded">https://api.autoclipai.com</code>
                        <h3 className="font-semibold text-sm mt-4 mb-2">Authentication</h3>
                        <p className="text-xs text-muted-foreground">Use Bearer token in the Authorization header: <code className="text-primary bg-primary/5 px-1 rounded">Authorization: Bearer YOUR_TOKEN</code></p>
                    </div>

                    <h2 className="text-2xl font-bold mb-6">Endpoints</h2>
                    <div className="space-y-3">
                        {endpoints.map((ep, i) => (
                            <Card key={i} className="bg-card border-border">
                                <CardContent className="p-4">
                                    <div className="flex items-center gap-3 mb-2">
                                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${ep.method === "GET" ? "bg-blue-500/10 text-blue-400" : "bg-green-500/10 text-green-400"}`}>
                                            {ep.method}
                                        </span>
                                        <code className="text-sm font-mono text-foreground">{ep.path}</code>
                                    </div>
                                    <p className="text-xs text-muted-foreground">{ep.desc}</p>
                                    {ep.body && (
                                        <pre className="mt-2 bg-background/50 border border-border rounded p-2 overflow-x-auto">
                                            <code className="text-xs text-primary font-mono">{ep.body}</code>
                                        </pre>
                                    )}
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    <div className="text-center mt-12">
                        <p className="text-sm text-muted-foreground">Need API access? <Link href="/contact" className="text-primary hover:underline">Contact us</Link> for a Business plan.</p>
                    </div>
                </div>
            </section>
        </div>
    );
}
