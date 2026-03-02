"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Scissors } from "lucide-react";

export function Navbar() {
    return (
        <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-xl">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2.5 group">
                        <div className="rounded-lg bg-primary/10 p-1.5 ring-1 ring-primary/30 group-hover:ring-primary/60 transition-all">
                            <Scissors className="h-5 w-5 text-primary" />
                        </div>
                        <span className="text-lg font-bold tracking-tight">
                            AutoClip<span className="text-primary">AI</span>
                        </span>
                    </Link>

                    {/* Nav Links */}
                    <div className="hidden md:flex items-center gap-6 text-sm text-muted-foreground">
                        <Link href="#features" className="hover:text-foreground transition-colors">Features</Link>
                        <Link href="#how-it-works" className="hover:text-foreground transition-colors">How it Works</Link>
                        <Link href="#pricing" className="hover:text-foreground transition-colors">Pricing</Link>
                        <Link href="#faq" className="hover:text-foreground transition-colors">FAQ</Link>
                    </div>

                    {/* CTA */}
                    <div className="flex items-center gap-3">
                        <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground" asChild>
                            <Link href="/dashboard">Login</Link>
                        </Button>
                        <Button size="sm" className="bg-primary text-primary-foreground hover:bg-primary/90 glow-green font-semibold" asChild>
                            <Link href="/dashboard">Get Started Free</Link>
                        </Button>
                    </div>
                </div>
            </div>
        </nav>
    );
}
