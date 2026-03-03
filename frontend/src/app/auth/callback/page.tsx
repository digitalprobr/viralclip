"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { verifyMagicLink, setAccessToken } from "@/lib/api";
import { Loader2, CheckCircle2, XCircle, Sparkles } from "lucide-react";
import Link from "next/link";

export default function AuthCallbackPage() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
    const [message, setMessage] = useState("");

    useEffect(() => {
        const token = searchParams.get("token");
        if (!token) {
            setStatus("error");
            setMessage("No magic link token found.");
            return;
        }

        verifyMagicLink(token)
            .then((result) => {
                setAccessToken(result.access_token);
                setStatus("success");
                setMessage(`Welcome, ${result.user.email}!`);
                setTimeout(() => router.push("/dashboard"), 2000);
            })
            .catch((err) => {
                setStatus("error");
                setMessage(err.message || "Invalid or expired magic link.");
            });
    }, [searchParams, router]);

    return (
        <div className="min-h-screen flex items-center justify-center px-4" style={{ background: "linear-gradient(to bottom, #0f1117 0%, #111827 100%)" }}>
            <div className="text-center">
                {/* Logo */}
                <Link href="/" className="inline-flex items-center gap-2 text-2xl font-extrabold mb-10">
                    <Sparkles className="h-7 w-7 text-primary" />
                    <span>Viral<span className="text-primary">Clip</span></span>
                </Link>

                {status === "loading" && (
                    <div className="space-y-4">
                        <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
                        <p className="text-lg text-muted-foreground">Verifying your magic link...</p>
                    </div>
                )}

                {status === "success" && (
                    <div className="space-y-4">
                        <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                            <CheckCircle2 className="h-8 w-8 text-primary" />
                        </div>
                        <h2 className="text-2xl font-bold text-foreground">You&apos;re in! 🎉</h2>
                        <p className="text-muted-foreground">{message}</p>
                        <p className="text-sm text-muted-foreground">Redirecting to dashboard...</p>
                    </div>
                )}

                {status === "error" && (
                    <div className="space-y-4">
                        <div className="w-16 h-16 rounded-full bg-red-500/10 flex items-center justify-center mx-auto">
                            <XCircle className="h-8 w-8 text-red-400" />
                        </div>
                        <h2 className="text-2xl font-bold text-foreground">Link expired</h2>
                        <p className="text-muted-foreground">{message}</p>
                        <Link
                            href="/auth/login"
                            className="inline-block mt-4 px-6 py-3 bg-primary text-primary-foreground rounded-xl font-semibold hover:bg-primary/90 transition"
                        >
                            Try again
                        </Link>
                    </div>
                )}
            </div>
        </div>
    );
}
