"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login, setAccessToken } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Mail, Lock, ArrowRight, Sparkles, CheckCircle2, Loader2, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

export default function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const router = useRouter();

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!email || !password) return;

        setLoading(true);
        setError("");

        try {
            const result = await login(email, password);
            setAccessToken(result.access_token);
            router.push("/dashboard");
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Something went wrong");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center px-4" style={{ background: "linear-gradient(to bottom, #0f1117 0%, #111827 100%)" }}>
            <div className="w-full max-w-md">
                {/* Logo */}
                <div className="text-center mb-8">
                    <Link href="/" className="inline-flex items-center gap-2 text-2xl font-extrabold">
                        <Sparkles className="h-7 w-7 text-primary" />
                        <span>Auto<span className="text-primary">Clip</span>AI</span>
                    </Link>
                </div>

                <Card className="bg-card/80 backdrop-blur-xl border-border">
                    <CardHeader className="text-center pb-2">
                        <CardTitle className="text-2xl">Welcome back</CardTitle>
                        <CardDescription>
                            Sign in to your account to continue
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            {/* Email */}
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-foreground">Email</label>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        type="email"
                                        placeholder="you@example.com"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="pl-10 h-12"
                                        required
                                    />
                                </div>
                            </div>

                            {/* Password */}
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-foreground">Password</label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        type={showPassword ? "text" : "password"}
                                        placeholder="Enter your password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="pl-10 pr-10 h-12"
                                        required
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                                    >
                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                </div>
                            </div>

                            {error && (
                                <p className="text-sm text-red-400 bg-red-400/10 rounded-lg p-3">
                                    {error}
                                </p>
                            )}

                            <Button
                                type="submit"
                                className="w-full h-12 text-base font-semibold bg-primary text-primary-foreground hover:bg-primary/90"
                                disabled={loading}
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Signing in...
                                    </>
                                ) : (
                                    <>
                                        Sign In
                                        <ArrowRight className="ml-2 h-4 w-4" />
                                    </>
                                )}
                            </Button>
                        </form>

                        <div className="mt-6 text-center">
                            <p className="text-sm text-muted-foreground">
                                Don&apos;t have an account?{" "}
                                <Link href="/auth/register" className="text-primary hover:underline font-medium">
                                    Create one
                                </Link>
                            </p>
                        </div>

                        <div className="mt-4 space-y-2">
                            <div className="flex items-center gap-2 justify-center text-xs text-muted-foreground">
                                <CheckCircle2 className="h-3.5 w-3.5 text-primary shrink-0" />
                                <span>New users get <strong className="text-primary">50 free credits</strong></span>
                            </div>
                            <div className="flex items-center gap-2 justify-center text-xs text-muted-foreground">
                                <CheckCircle2 className="h-3.5 w-3.5 text-primary shrink-0" />
                                <span>Works with Gmail, Hotmail, Yahoo, or any email</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
