"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signup, setAccessToken } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { User, Lock, Mail, ArrowRight, Sparkles, CheckCircle2, XCircle, Loader2, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

const PASSWORD_RULES = [
    { label: "At least 8 characters", test: (p: string) => p.length >= 8 },
    { label: "One uppercase letter (A-Z)", test: (p: string) => /[A-Z]/.test(p) },
    { label: "One lowercase letter (a-z)", test: (p: string) => /[a-z]/.test(p) },
    { label: "One digit (0-9)", test: (p: string) => /[0-9]/.test(p) },
    { label: "One special character (!@#$%^&*)", test: (p: string) => /[!@#$%^&*()_+\-=[\]{};:'",.<>?/\\|`~]/.test(p) },
];

export default function RegisterPage() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirm, setShowConfirm] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const router = useRouter();

    const passedRules = PASSWORD_RULES.filter(r => r.test(password));
    const allRulesPassed = passedRules.length === PASSWORD_RULES.length;
    const passwordsMatch = password === confirmPassword && confirmPassword.length > 0;

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!allRulesPassed) return;
        if (!passwordsMatch) {
            setError("Passwords do not match");
            return;
        }

        setLoading(true);
        setError("");

        try {
            const result = await signup({
                username,
                email,
                password,
                confirm_password: confirmPassword,
            });
            setAccessToken(result.access_token);
            router.push("/dashboard");
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Something went wrong");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center px-4 py-12" style={{ background: "linear-gradient(to bottom, #0f1117 0%, #111827 100%)" }}>
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
                        <CardTitle className="text-2xl">Create your account</CardTitle>
                        <CardDescription>
                            Get 50 free credits to start creating viral clips
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            {/* Username */}
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-foreground">Username</label>
                                <div className="relative">
                                    <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        type="text"
                                        placeholder="johndoe"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        className="pl-10 h-11"
                                        required
                                        minLength={3}
                                        maxLength={30}
                                    />
                                </div>
                            </div>

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
                                        className="pl-10 h-11"
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
                                        placeholder="Create a strong password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="pl-10 pr-10 h-11"
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

                                {/* Password strength rules */}
                                {password.length > 0 && (
                                    <div className="mt-2 space-y-1 p-3 rounded-lg bg-card/50 border border-border/50">
                                        {PASSWORD_RULES.map((rule, i) => {
                                            const passed = rule.test(password);
                                            return (
                                                <div key={i} className={`flex items-center gap-2 text-xs transition-colors ${passed ? 'text-primary' : 'text-muted-foreground'}`}>
                                                    {passed ? (
                                                        <CheckCircle2 className="h-3.5 w-3.5 shrink-0" />
                                                    ) : (
                                                        <XCircle className="h-3.5 w-3.5 shrink-0" />
                                                    )}
                                                    <span>{rule.label}</span>
                                                </div>
                                            );
                                        })}
                                    </div>
                                )}
                            </div>

                            {/* Confirm Password */}
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-foreground">Confirm Password</label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        type={showConfirm ? "text" : "password"}
                                        placeholder="Confirm your password"
                                        value={confirmPassword}
                                        onChange={(e) => setConfirmPassword(e.target.value)}
                                        className="pl-10 pr-10 h-11"
                                        required
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowConfirm(!showConfirm)}
                                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                                    >
                                        {showConfirm ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                </div>
                                {confirmPassword.length > 0 && !passwordsMatch && (
                                    <p className="text-xs text-red-400 mt-1 flex items-center gap-1">
                                        <XCircle className="h-3 w-3" /> Passwords do not match
                                    </p>
                                )}
                                {passwordsMatch && (
                                    <p className="text-xs text-primary mt-1 flex items-center gap-1">
                                        <CheckCircle2 className="h-3 w-3" /> Passwords match
                                    </p>
                                )}
                            </div>

                            {error && (
                                <p className="text-sm text-red-400 bg-red-400/10 rounded-lg p-3">
                                    {error}
                                </p>
                            )}

                            <Button
                                type="submit"
                                className="w-full h-12 text-base font-semibold bg-primary text-primary-foreground hover:bg-primary/90"
                                disabled={loading || !allRulesPassed || !passwordsMatch}
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Creating account...
                                    </>
                                ) : (
                                    <>
                                        Create Account
                                        <ArrowRight className="ml-2 h-4 w-4" />
                                    </>
                                )}
                            </Button>
                        </form>

                        <div className="mt-6 text-center">
                            <p className="text-sm text-muted-foreground">
                                Already have an account?{" "}
                                <Link href="/auth/login" className="text-primary hover:underline font-medium">
                                    Sign in
                                </Link>
                            </p>
                        </div>

                        <div className="mt-4 flex items-center gap-2 justify-center text-xs text-muted-foreground">
                            <CheckCircle2 className="h-3.5 w-3.5 text-primary shrink-0" />
                            <span>New users get <strong className="text-primary">50 free credits</strong></span>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
