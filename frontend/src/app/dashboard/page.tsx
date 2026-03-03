"use client";

import { useCallback, useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Navbar } from "@/components/navbar";
import {
    submitClipJob, listJobs, getMe, checkHealth, subscribeToProgress,
    getClipFiles, getFileUrl,
    User, JobResponse, ProgressEvent, ClipFile,
} from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import {
    Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import {
    Play, Loader2, Scissors, CreditCard, CheckCircle2, XCircle, Clock,
    ChevronDown, ChevronUp, Download, Film, Wifi, WifiOff, RefreshCw,
    Sparkles, ArrowRight,
} from "lucide-react";

// ── Types ──────────────────────────────────────────────

type ActiveJob = {
    jobId: number;
    taskId: string;
    progress: ProgressEvent | null;
    logs: string[];
    showLogs: boolean;
    clips: ClipFile[];
};

// ── Page ────────────────────────────────────────────────

export default function DashboardPage() {
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(false);
    const [apiOnline, setApiOnline] = useState<boolean | null>(null);

    // Form state
    const [url, setUrl] = useState("");
    const [engine, setEngine] = useState("auto");
    const [numClips, setNumClips] = useState("");

    // Jobs
    const [jobs, setJobs] = useState<JobResponse[]>([]);
    const [activeJobs, setActiveJobs] = useState<Map<number, ActiveJob>>(new Map());
    const cleanupRefs = useRef<Map<string, () => void>>(new Map());

    // ── Auth check ──────────────────────────────────────

    useEffect(() => {
        getMe().then((u) => {
            if (!u) {
                router.push("/auth/login");
                return;
            }
            setUser(u);
        });
        checkHealth().then(setApiOnline);
    }, [router]);

    // ── Load jobs ───────────────────────────────────────

    const refreshJobs = useCallback(async () => {
        const data = await listJobs();
        setJobs(data);
    }, []);

    useEffect(() => {
        if (user) refreshJobs();
    }, [user, refreshJobs]);

    // ── Submit ──────────────────────────────────────────

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!url || !user) return;

        if (user.credits < 10) {
            toast.error("Insufficient credits! You need at least 10 credits.");
            return;
        }

        setLoading(true);
        try {
            const result = await submitClipJob({
                url,
                preferred_engine: engine,
                num_clips: numClips ? parseInt(numClips) : undefined,
            });

            toast.success(`Job submitted! ${result.credits_remaining} credits remaining.`);
            setUser((prev) => prev ? { ...prev, credits: result.credits_remaining } : prev);
            setUrl("");

            // Start SSE tracking
            const jobData: ActiveJob = {
                jobId: result.job_id,
                taskId: result.task_id,
                progress: null,
                logs: [],
                showLogs: false,
                clips: [],
            };

            setActiveJobs((prev) => new Map(prev).set(result.job_id, jobData));

            const cleanup = subscribeToProgress(
                result.task_id,
                (event) => {
                    setActiveJobs((prev) => {
                        const next = new Map(prev);
                        const job = next.get(result.job_id);
                        if (job) {
                            job.progress = event;
                            if (event.logs) {
                                job.logs = [...job.logs, ...event.logs.filter((l) => !job.logs.includes(l))];
                            }
                        }
                        return next;
                    });
                },
                async () => {
                    // On complete: fetch clip files
                    try {
                        const clipData = await getClipFiles(result.job_id);
                        setActiveJobs((prev) => {
                            const next = new Map(prev);
                            const job = next.get(result.job_id);
                            if (job) job.clips = clipData.files;
                            return next;
                        });
                    } catch { }
                    refreshJobs();
                    getMe().then(setUser);
                },
            );

            cleanupRefs.current.set(result.task_id, cleanup);
            refreshJobs();
        } catch (err: any) {
            toast.error(err.message || "Failed to submit job");
        } finally {
            setLoading(false);
        }
    }

    // ── Cleanup SSE on unmount ──────────────────────────

    useEffect(() => {
        return () => {
            cleanupRefs.current.forEach((cleanup) => cleanup());
        };
    }, []);

    // ── Toggle logs ─────────────────────────────────────

    const toggleLogs = (jobId: number) => {
        setActiveJobs((prev) => {
            const next = new Map(prev);
            const job = next.get(jobId);
            if (job) job.showLogs = !job.showLogs;
            return next;
        });
    };

    // ── Render ──────────────────────────────────────────

    if (!user) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="min-h-screen">
            <Navbar />
            <div className="mx-auto max-w-6xl px-4 py-10">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold">Dashboard</h1>
                        <p className="text-muted-foreground mt-1">Submit videos and manage your clipping jobs.</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <Badge variant="outline" className="h-8 px-3 gap-1.5 border-primary/30 bg-primary/5">
                            <CreditCard className="h-3.5 w-3.5 text-primary" />
                            <span className="text-primary font-bold">{user.credits}</span>
                            <span className="text-muted-foreground/70 text-xs">credits</span>
                        </Badge>
                        <div className="flex items-center gap-2">
                            {apiOnline ? (
                                <><Wifi className="h-4 w-4 text-emerald-400" /><span className="text-xs text-emerald-400">Online</span></>
                            ) : (
                                <><WifiOff className="h-4 w-4 text-red-400" /><span className="text-xs text-red-400">Offline</span></>
                            )}
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* ── Submit Form ──────────── */}
                    <div className="lg:col-span-2">
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Sparkles className="h-5 w-5 text-primary" />
                                    New Clip Job
                                </CardTitle>
                                <CardDescription>Paste a YouTube URL and configure your clipping parameters. Costs 10 credits.</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <form onSubmit={handleSubmit} className="space-y-5">
                                    {/* URL */}
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">YouTube Video URL</label>
                                        <div className="relative">
                                            <Play className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                            <Input
                                                placeholder="https://www.youtube.com/watch?v=..."
                                                value={url}
                                                onChange={(e) => setUrl(e.target.value)}
                                                className="pl-10 h-12"
                                                required
                                            />
                                        </div>
                                    </div>

                                    {/* Engine + Clips */}
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <label className="text-sm font-medium">AI Engine</label>
                                            <Select value={engine} onValueChange={setEngine}>
                                                <SelectTrigger className="h-11">
                                                    <SelectValue />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="auto">Auto (Best Available)</SelectItem>
                                                    <SelectItem value="gemini">Gemini 2.0 Flash</SelectItem>
                                                    <SelectItem value="deepseek">DeepSeek V3</SelectItem>
                                                    <SelectItem value="groq">Groq Llama 3.3</SelectItem>
                                                    <SelectItem value="qwen">Alibaba Qwen</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-sm font-medium">Number of Clips</label>
                                            <Input
                                                placeholder="Auto (3-7)"
                                                type="number"
                                                min={1}
                                                max={15}
                                                value={numClips}
                                                onChange={(e) => setNumClips(e.target.value)}
                                                className="h-11"
                                            />
                                        </div>
                                    </div>

                                    <Button
                                        type="submit"
                                        disabled={loading || apiOnline === false || user.credits < 10}
                                        className="w-full h-12 text-base font-semibold bg-primary text-primary-foreground hover:bg-primary/90"
                                    >
                                        {loading ? (
                                            <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Processing...</>
                                        ) : user.credits < 10 ? (
                                            <><CreditCard className="mr-2 h-4 w-4" /> Insufficient Credits</>
                                        ) : (
                                            <><Scissors className="mr-2 h-4 w-4" /> Generate Viral Clips — 10 credits</>
                                        )}
                                    </Button>
                                </form>
                            </CardContent>
                        </Card>
                    </div>

                    {/* ── Sidebar ──────────────── */}
                    <div className="space-y-6">
                        <Card>
                            <CardHeader><CardTitle className="text-base">⚡ Quick Stats</CardTitle></CardHeader>
                            <CardContent className="space-y-3">
                                <div className="flex justify-between text-sm">
                                    <span className="text-muted-foreground">Credits</span>
                                    <span className="font-bold text-primary">{user.credits}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-muted-foreground">Total Jobs</span>
                                    <span className="font-bold">{jobs.length}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-muted-foreground">Completed</span>
                                    <span className="font-bold text-emerald-400">{jobs.filter((j) => j.status === "SUCCESS").length}</span>
                                </div>
                                <Separator />
                                <Button variant="outline" size="sm" className="w-full" onClick={refreshJobs}>
                                    <RefreshCw className="mr-2 h-3.5 w-3.5" /> Refresh
                                </Button>
                            </CardContent>
                        </Card>
                    </div>
                </div>

                {/* ── Active Jobs with Progress ────── */}
                {activeJobs.size > 0 && (
                    <div className="mt-10 space-y-4">
                        <h2 className="text-xl font-bold flex items-center gap-2">
                            <Loader2 className="h-5 w-5 animate-spin text-primary" />
                            Active Processing
                        </h2>
                        {Array.from(activeJobs.entries()).map(([jobId, job]) => (
                            <Card key={jobId} className="overflow-hidden">
                                <CardContent className="py-5">
                                    {/* Progress Bar */}
                                    <div className="space-y-3">
                                        <div className="flex items-center justify-between">
                                            <span className="text-sm font-medium">
                                                {job.progress?.step || "Waiting in queue..."}
                                            </span>
                                            <span className="text-sm font-bold text-primary">
                                                {Math.round(job.progress?.progress || 0)}%
                                            </span>
                                        </div>
                                        <Progress value={job.progress?.progress || 0} className="h-3" />

                                        {/* Status badge */}
                                        <div className="flex items-center justify-between">
                                            <Badge variant={
                                                job.progress?.status === "SUCCESS" ? "default" :
                                                    job.progress?.status === "FAILURE" ? "destructive" : "secondary"
                                            }>
                                                {job.progress?.status || "PENDING"}
                                            </Badge>

                                            {/* Toggle logs */}
                                            <button
                                                onClick={() => toggleLogs(jobId)}
                                                className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
                                            >
                                                {job.showLogs ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                                                {job.showLogs ? "Hide logs" : "Show logs"}
                                            </button>
                                        </div>

                                        {/* Expandable Logs */}
                                        {job.showLogs && (
                                            <div className="mt-3 bg-black/50 rounded-lg p-4 max-h-48 overflow-y-auto font-mono text-xs text-green-400 space-y-1">
                                                {job.logs.length > 0 ? (
                                                    job.logs.map((log, i) => <div key={i}>{log}</div>)
                                                ) : (
                                                    <div className="text-muted-foreground">Waiting for logs...</div>
                                                )}
                                            </div>
                                        )}

                                        {/* Video Preview (when completed) */}
                                        {job.clips.length > 0 && (
                                            <div className="mt-4 space-y-3">
                                                <h3 className="text-sm font-semibold flex items-center gap-2">
                                                    <Film className="h-4 w-4 text-primary" />
                                                    Generated Clips ({job.clips.length})
                                                </h3>
                                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                                    {job.clips.map((clip, i) => (
                                                        <div key={i} className="bg-card border border-border rounded-xl overflow-hidden">
                                                            <video
                                                                src={getFileUrl(clip.url)}
                                                                controls
                                                                className="w-full aspect-[9/16] object-cover bg-black"
                                                                preload="metadata"
                                                            />
                                                            <div className="p-3 space-y-2">
                                                                <p className="text-xs font-medium truncate">{clip.name}</p>
                                                                <div className="flex items-center justify-between">
                                                                    <Badge variant="outline" className="text-xs">
                                                                        {clip.platform}
                                                                    </Badge>
                                                                    <a
                                                                        href={getFileUrl(clip.url)}
                                                                        download
                                                                        className="text-xs text-primary hover:underline flex items-center gap-1"
                                                                    >
                                                                        <Download className="h-3 w-3" /> Download
                                                                    </a>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                )}

                {/* ── Job History ─────────────────── */}
                <div className="mt-10">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <Film className="h-5 w-5" />
                        Job History
                    </h2>

                    {jobs.length === 0 ? (
                        <Card>
                            <CardContent className="py-12 text-center">
                                <Scissors className="h-12 w-12 text-muted-foreground/30 mx-auto mb-3" />
                                <p className="text-muted-foreground">No jobs yet. Submit a YouTube URL above to get started!</p>
                            </CardContent>
                        </Card>
                    ) : (
                        <div className="space-y-3">
                            {jobs.map((job) => (
                                <Card key={job.id} className="hover:border-primary/30 transition-colors">
                                    <CardContent className="py-4">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-3 min-w-0">
                                                {job.status === "SUCCESS" ? (
                                                    <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" />
                                                ) : job.status === "FAILURE" ? (
                                                    <XCircle className="h-5 w-5 text-red-400 shrink-0" />
                                                ) : (
                                                    <Clock className="h-5 w-5 text-yellow-400 shrink-0" />
                                                )}
                                                <div className="min-w-0">
                                                    <p className="text-sm font-medium truncate">{job.url}</p>
                                                    <p className="text-xs text-muted-foreground">
                                                        {new Date(job.created_at).toLocaleDateString()} · {job.engine} · {job.credits_used} credits
                                                    </p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Badge variant={
                                                    job.status === "SUCCESS" ? "default" :
                                                        job.status === "FAILURE" ? "destructive" : "secondary"
                                                }>
                                                    {job.status}
                                                </Badge>
                                                {job.status === "SUCCESS" && (
                                                    <Button
                                                        variant="ghost"
                                                        size="sm"
                                                        onClick={async () => {
                                                            const clipData = await getClipFiles(job.id);
                                                            if (clipData.files.length > 0) {
                                                                setActiveJobs((prev) => {
                                                                    const next = new Map(prev);
                                                                    next.set(job.id, {
                                                                        jobId: job.id,
                                                                        taskId: job.celery_task_id || "",
                                                                        progress: { progress: 100, step: "✅ Completed!", status: "SUCCESS" },
                                                                        logs: [],
                                                                        showLogs: false,
                                                                        clips: clipData.files,
                                                                    });
                                                                    return next;
                                                                });
                                                            }
                                                        }}
                                                    >
                                                        <Film className="h-4 w-4 mr-1" /> View Clips
                                                    </Button>
                                                )}
                                            </div>
                                        </div>
                                        {job.error_message && (
                                            <p className="text-xs text-red-400 mt-2 bg-red-400/10 rounded-lg p-2">
                                                {job.error_message}
                                            </p>
                                        )}
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
