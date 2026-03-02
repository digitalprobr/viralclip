"use client";

import { useState, useEffect, useCallback } from "react";
import { Navbar } from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Scissors, Play, Zap, Activity, CheckCircle2, Clock, AlertCircle,
    Loader2, Plus, RotateCcw, ExternalLink, FolderOpen
} from "lucide-react";
import { toast } from "sonner";
import { submitClipJob, getTaskStatus, checkHealth } from "@/lib/api";
import type { TaskStatus } from "@/lib/api";

/* ─── Types ─── */
interface Job {
    taskId: string;
    url: string;
    engine: string;
    submittedAt: Date;
    status: string;
    result?: TaskStatus["result"];
    error?: string;
}

/* ─── Status Helpers ─── */
function statusColor(s: string) {
    switch (s) {
        case "SUCCESS": return "text-primary";
        case "FAILURE": return "text-destructive";
        case "STARTED": case "PENDING": return "text-yellow-500";
        default: return "text-muted-foreground";
    }
}
function statusIcon(s: string) {
    switch (s) {
        case "SUCCESS": return <CheckCircle2 className="h-4 w-4" />;
        case "FAILURE": return <AlertCircle className="h-4 w-4" />;
        case "STARTED": return <Loader2 className="h-4 w-4 animate-spin" />;
        case "PENDING": return <Clock className="h-4 w-4" />;
        default: return <Clock className="h-4 w-4" />;
    }
}

/* ═══════════════════════════════════════════════════════
   DASHBOARD PAGE
   ═══════════════════════════════════════════════════════ */
export default function DashboardPage() {
    const [url, setUrl] = useState("");
    const [engine, setEngine] = useState("auto");
    const [numClips, setNumClips] = useState("");
    const [loading, setLoading] = useState(false);
    const [jobs, setJobs] = useState<Job[]>([]);
    const [apiOnline, setApiOnline] = useState<boolean | null>(null);

    /* Health check */
    useEffect(() => {
        checkHealth()
            .then(() => setApiOnline(true))
            .catch(() => setApiOnline(false));
    }, []);

    /* Poll active jobs */
    const pollJobs = useCallback(async () => {
        const activeJobs = jobs.filter(j => j.status === "PENDING" || j.status === "STARTED");
        for (const job of activeJobs) {
            try {
                const status = await getTaskStatus(job.taskId);
                setJobs(prev => prev.map(j =>
                    j.taskId === job.taskId
                        ? { ...j, status: status.task_status, result: status.result, error: status.error }
                        : j
                ));
                if (status.task_status === "SUCCESS") {
                    toast.success(`Clip job completed: ${job.url.slice(0, 40)}...`);
                } else if (status.task_status === "FAILURE") {
                    toast.error(`Clip job failed: ${status.error || "Unknown error"}`);
                }
            } catch { /* silently retry */ }
        }
    }, [jobs]);

    useEffect(() => {
        const interval = setInterval(pollJobs, 3000);
        return () => clearInterval(interval);
    }, [pollJobs]);

    /* Submit */
    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!url.trim()) { toast.error("Please enter a YouTube URL"); return; }

        setLoading(true);
        try {
            const res = await submitClipJob({
                url: url.trim(),
                preferred_engine: engine,
                num_clips: numClips ? parseInt(numClips) : undefined,
            });
            setJobs(prev => [{
                taskId: res.task_id,
                url: url.trim(),
                engine,
                submittedAt: new Date(),
                status: "PENDING",
            }, ...prev]);
            toast.success("Video submitted to the clipping queue!");
            setUrl("");
            setNumClips("");
        } catch (err) {
            toast.error(`Submission failed: ${err instanceof Error ? err.message : "Network error"}`);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen">
            <Navbar />

            <div className="mx-auto max-w-6xl px-4 py-10">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-extrabold tracking-tight">Dashboard</h1>
                        <p className="text-muted-foreground mt-1">Submit videos and manage your clipping jobs.</p>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                        <span className={`w-2 h-2 rounded-full ${apiOnline === true ? 'bg-primary animate-pulse' : apiOnline === false ? 'bg-destructive' : 'bg-muted-foreground'}`} />
                        <span className="text-muted-foreground">
                            API {apiOnline === true ? 'Online' : apiOnline === false ? 'Offline' : 'Checking...'}
                        </span>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* ─── Left: Submit Form ─── */}
                    <div className="lg:col-span-2">
                        <Card className="bg-card border-border">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Plus className="h-5 w-5 text-primary" />
                                    New Clip Job
                                </CardTitle>
                                <CardDescription>Paste a YouTube URL and configure your clipping parameters.</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <form onSubmit={handleSubmit} className="space-y-5">
                                    <div className="space-y-2">
                                        <Label htmlFor="url">YouTube Video URL</Label>
                                        <div className="flex items-center gap-2">
                                            <div className="flex items-center flex-1 gap-2 px-4 py-0 rounded-xl border border-border bg-input h-12">
                                                <Play className="h-4 w-4 text-muted-foreground shrink-0" />
                                                <Input
                                                    id="url"
                                                    value={url}
                                                    onChange={e => setUrl(e.target.value)}
                                                    placeholder="https://www.youtube.com/watch?v=..."
                                                    className="border-0 bg-transparent focus-visible:ring-0 shadow-none h-10"
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label htmlFor="engine">AI Engine</Label>
                                            <select
                                                id="engine"
                                                value={engine}
                                                onChange={e => setEngine(e.target.value)}
                                                className="w-full h-10 px-3 rounded-lg border border-border bg-input text-sm text-foreground focus:ring-2 focus:ring-primary/40 appearance-none"
                                            >
                                                <option value="auto">Auto (Best Available)</option>
                                                <option value="gemini">Gemini 2.0 Flash</option>
                                                <option value="deepseek">DeepSeek V3</option>
                                                <option value="groq">Groq Llama 3.3</option>
                                                <option value="qwen">Alibaba Qwen Plus</option>
                                            </select>
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="clips">Number of Clips</Label>
                                            <Input
                                                id="clips"
                                                type="number"
                                                min={1}
                                                max={10}
                                                value={numClips}
                                                onChange={e => setNumClips(e.target.value)}
                                                placeholder="Auto (3-7)"
                                                className="bg-input h-10"
                                            />
                                        </div>
                                    </div>

                                    <Button
                                        type="submit"
                                        disabled={loading || apiOnline === false}
                                        className="w-full h-12 bg-primary text-primary-foreground hover:bg-primary/90 font-semibold text-base glow-green"
                                    >
                                        {loading ? (
                                            <><Loader2 className="mr-2 h-5 w-5 animate-spin" /> Processing...</>
                                        ) : (
                                            <><Scissors className="mr-2 h-5 w-5" /> Generate Viral Clips</>
                                        )}
                                    </Button>
                                </form>
                            </CardContent>
                        </Card>
                    </div>

                    {/* ─── Right: System Status ─── */}
                    <div className="space-y-6">
                        <Card className="bg-card border-border">
                            <CardHeader className="pb-3">
                                <CardTitle className="text-base flex items-center gap-2">
                                    <Activity className="h-4 w-4 text-primary" />
                                    System Status
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-3 text-sm">
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">API Backend</span>
                                    <span className={apiOnline ? 'text-primary font-medium' : 'text-destructive font-medium'}>
                                        {apiOnline === true ? '● Online' : apiOnline === false ? '● Offline' : '○ Checking'}
                                    </span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">Active Jobs</span>
                                    <span className="font-medium">
                                        {jobs.filter(j => j.status === "PENDING" || j.status === "STARTED").length}
                                    </span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">Completed</span>
                                    <span className="text-primary font-medium">
                                        {jobs.filter(j => j.status === "SUCCESS").length}
                                    </span>
                                </div>
                            </CardContent>
                        </Card>

                        <Card className="bg-card border-border">
                            <CardHeader className="pb-3">
                                <CardTitle className="text-base flex items-center gap-2">
                                    <Zap className="h-4 w-4 text-accent" />
                                    Quick Actions
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-2">
                                <Button variant="outline" size="sm" className="w-full justify-start" onClick={pollJobs}>
                                    <RotateCcw className="mr-2 h-4 w-4" /> Refresh All Jobs
                                </Button>
                                <Button variant="outline" size="sm" className="w-full justify-start" asChild>
                                    <a href="http://localhost:8080/docs" target="_blank" rel="noopener noreferrer">
                                        <ExternalLink className="mr-2 h-4 w-4" /> API Documentation
                                    </a>
                                </Button>
                            </CardContent>
                        </Card>
                    </div>
                </div>

                {/* ─── Job History ─── */}
                <div className="mt-10">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <FolderOpen className="h-5 w-5 text-muted-foreground" />
                        Job History
                    </h2>

                    {jobs.length === 0 ? (
                        <Card className="bg-card border-border">
                            <CardContent className="py-12 text-center text-muted-foreground">
                                <Scissors className="h-10 w-10 mx-auto mb-3 opacity-30" />
                                <p className="text-sm">No jobs yet. Submit a YouTube URL above to get started!</p>
                            </CardContent>
                        </Card>
                    ) : (
                        <div className="space-y-3">
                            {jobs.map(job => (
                                <Card key={job.taskId} className="bg-card border-border hover:border-border/80 transition-colors">
                                    <CardContent className="py-4 flex items-center justify-between">
                                        <div className="flex items-center gap-4 min-w-0">
                                            <div className={`${statusColor(job.status)}`}>
                                                {statusIcon(job.status)}
                                            </div>
                                            <div className="min-w-0">
                                                <p className="text-sm font-medium truncate max-w-md">{job.url}</p>
                                                <p className="text-xs text-muted-foreground mt-0.5">
                                                    {job.engine.toUpperCase()} · {job.submittedAt.toLocaleTimeString()}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-3">
                                            <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${job.status === "SUCCESS" ? "border-primary/30 bg-primary/10 text-primary" :
                                                    job.status === "FAILURE" ? "border-destructive/30 bg-destructive/10 text-destructive" :
                                                        "border-yellow-500/30 bg-yellow-500/10 text-yellow-500"
                                                }`}>
                                                {job.status}
                                            </span>
                                            {job.result && (
                                                <Button variant="ghost" size="sm" className="text-xs">
                                                    <FolderOpen className="mr-1 h-3 w-3" /> View Clips
                                                </Button>
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
