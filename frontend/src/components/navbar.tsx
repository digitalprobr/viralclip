"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { Sparkles, LogOut, CreditCard, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getMe, logout, User } from "@/lib/api";

export function Navbar() {
    const pathname = usePathname();
    const [user, setUser] = useState<User | null>(null);
    const [mobileOpen, setMobileOpen] = useState(false);
    const isLanding = pathname === "/";

    useEffect(() => {
        getMe().then(setUser).catch(() => setUser(null));
    }, [pathname]);

    const handleLogout = async () => {
        await logout();
        setUser(null);
        window.location.href = "/";
    };

    const navLinks = isLanding
        ? [
            { label: "Features", href: "#features" },
            { label: "How it Works", href: "#how-it-works" },
            { label: "Pricing", href: "#pricing" },
        ]
        : [
            { label: "Dashboard", href: "/dashboard" },
        ];

    const handleAnchorClick = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
        if (href.startsWith("#")) {
            e.preventDefault();
            const el = document.querySelector(href);
            if (el) {
                el.scrollIntoView({ behavior: "smooth", block: "start" });
            }
            setMobileOpen(false);
        }
    };

    return (
        <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-xl">
            <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
                {/* Logo */}
                <Link href="/" className="flex items-center gap-2 text-xl font-extrabold">
                    <Sparkles className="h-6 w-6 text-primary" />
                    <span>
                        AutoClip<span className="text-primary">AI</span>
                    </span>
                </Link>

                {/* Desktop Nav */}
                <div className="hidden md:flex items-center gap-6">
                    {navLinks.map((link) => (
                        <a
                            key={link.href}
                            href={link.href}
                            onClick={(e) => handleAnchorClick(e, link.href)}
                            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                        >
                            {link.label}
                        </a>
                    ))}
                </div>

                {/* Auth / Credits */}
                <div className="hidden md:flex items-center gap-3">
                    {user ? (
                        <>
                            <Badge variant="outline" className="h-8 px-3 gap-1.5 border-primary/30 bg-primary/5">
                                <CreditCard className="h-3.5 w-3.5 text-primary" />
                                <span className="text-primary font-semibold">{user.credits}</span>
                                <span className="text-muted-foreground text-xs">credits</span>
                            </Badge>
                            <span className="text-sm text-muted-foreground">{user.email}</span>
                            <Button variant="ghost" size="sm" onClick={handleLogout} className="text-muted-foreground hover:text-foreground">
                                <LogOut className="h-4 w-4" />
                            </Button>
                        </>
                    ) : (
                        <>
                            <Button variant="ghost" size="sm" asChild>
                                <Link href="/auth/login">Login</Link>
                            </Button>
                            <Button size="sm" className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-full px-5" asChild>
                                <Link href="/auth/login">Get Started Free</Link>
                            </Button>
                        </>
                    )}
                </div>

                {/* Mobile Menu Button */}
                <button className="md:hidden" onClick={() => setMobileOpen(!mobileOpen)}>
                    {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                </button>
            </div>

            {/* Mobile Menu */}
            {mobileOpen && (
                <div className="md:hidden border-t border-border bg-background/95 backdrop-blur-xl px-4 py-4 space-y-3">
                    {navLinks.map((link) => (
                        <a
                            key={link.href}
                            href={link.href}
                            onClick={(e) => {
                                handleAnchorClick(e, link.href);
                                setMobileOpen(false);
                            }}
                            className="block text-sm text-muted-foreground hover:text-foreground py-2"
                        >
                            {link.label}
                        </a>
                    ))}
                    {user ? (
                        <div className="pt-2 border-t border-border flex items-center justify-between">
                            <Badge variant="outline" className="border-primary/30">
                                <CreditCard className="h-3 w-3 mr-1 text-primary" />
                                {user.credits} credits
                            </Badge>
                            <Button variant="ghost" size="sm" onClick={handleLogout}>
                                <LogOut className="h-4 w-4 mr-1" /> Logout
                            </Button>
                        </div>
                    ) : (
                        <Button className="w-full bg-primary text-primary-foreground" asChild>
                            <Link href="/auth/login">Get Started Free</Link>
                        </Button>
                    )}
                </div>
            )}
        </nav>
    );
}
