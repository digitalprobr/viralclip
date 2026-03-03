"use client";

import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, Clock, ArrowRight, BookOpen, Tag } from "lucide-react";
import Link from "next/link";
import { blogArticles, BLOG_CATEGORIES } from "./data";

export default function BlogPage() {
    const [search, setSearch] = useState("");
    const [activeCategory, setActiveCategory] = useState("All");

    const filtered = blogArticles.filter((a) => {
        const matchesSearch =
            a.title.toLowerCase().includes(search.toLowerCase()) ||
            a.excerpt.toLowerCase().includes(search.toLowerCase());
        const matchesCategory = activeCategory === "All" || a.category === activeCategory;
        return matchesSearch && matchesCategory;
    });

    return (
        <div className="min-h-screen">
            <Navbar />

            {/* Hero */}
            <section className="pt-20 pb-12 px-4 text-center">
                <div className="mx-auto max-w-3xl">
                    <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-4 py-1.5 text-sm text-primary mb-6">
                        <BookOpen className="h-4 w-4" />
                        AutoClip AI Blog
                    </div>
                    <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
                        Learn, Create, <span className="text-gradient">Grow</span>
                    </h1>
                    <p className="text-muted-foreground text-lg mb-8">
                        Guides, tutorials, and insights on AI video creation, faceless YouTube,
                        and content automation.
                    </p>

                    {/* Search */}
                    <div className="max-w-md mx-auto relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search articles..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="pl-10 h-12"
                        />
                    </div>
                </div>
            </section>

            {/* Categories */}
            <section className="px-4 pb-8">
                <div className="mx-auto max-w-5xl flex flex-wrap gap-2 justify-center">
                    {BLOG_CATEGORIES.map((cat) => (
                        <Button
                            key={cat}
                            variant={activeCategory === cat ? "default" : "outline"}
                            size="sm"
                            onClick={() => setActiveCategory(cat)}
                            className={activeCategory === cat ? "bg-primary text-primary-foreground" : ""}
                        >
                            {cat}
                        </Button>
                    ))}
                </div>
            </section>

            {/* Articles Grid */}
            <section className="px-4 pb-24">
                <div className="mx-auto max-w-5xl">
                    {filtered.length === 0 ? (
                        <div className="text-center py-16">
                            <p className="text-muted-foreground text-lg">No articles found matching your search.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {filtered.map((article) => (
                                <Link key={article.slug} href={`/blog/${article.slug}`}>
                                    <Card className="bg-card border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:shadow-primary/5 h-full group cursor-pointer">
                                        {/* Color banner */}
                                        <div className="h-2 bg-gradient-to-r from-primary to-emerald-400 rounded-t-lg" />
                                        <CardContent className="p-6">
                                            {/* Category + read time */}
                                            <div className="flex items-center justify-between mb-3">
                                                <span className="inline-flex items-center gap-1 text-xs font-medium text-primary bg-primary/10 px-2 py-1 rounded-full">
                                                    <Tag className="h-3 w-3" />
                                                    {article.category}
                                                </span>
                                                <span className="flex items-center gap-1 text-xs text-muted-foreground">
                                                    <Clock className="h-3 w-3" />
                                                    {article.readTime}
                                                </span>
                                            </div>

                                            {/* Title */}
                                            <h2 className="text-lg font-bold mb-2 group-hover:text-primary transition-colors line-clamp-2">
                                                {article.title}
                                            </h2>

                                            {/* Excerpt */}
                                            <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
                                                {article.excerpt}
                                            </p>

                                            {/* Footer */}
                                            <div className="flex items-center justify-between mt-auto pt-4 border-t border-border/50">
                                                <span className="text-xs text-muted-foreground">
                                                    {new Date(article.date).toLocaleDateString("en-US", {
                                                        month: "short",
                                                        day: "numeric",
                                                        year: "numeric",
                                                    })}
                                                </span>
                                                <span className="text-xs text-primary font-medium flex items-center gap-1 group-hover:gap-2 transition-all">
                                                    Read more <ArrowRight className="h-3 w-3" />
                                                </span>
                                            </div>
                                        </CardContent>
                                    </Card>
                                </Link>
                            ))}
                        </div>
                    )}
                </div>
            </section>

            {/* CTA */}
            <section className="px-4 pb-24">
                <div className="mx-auto max-w-3xl text-center bg-card/50 border border-border rounded-2xl p-12">
                    <h2 className="text-2xl font-bold mb-4">Ready to Create Viral Clips?</h2>
                    <p className="text-muted-foreground mb-6">
                        Start for free. Paste a YouTube URL and let AI do the rest.
                    </p>
                    <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90" asChild>
                        <Link href="/auth/register">
                            Get Started Free <ArrowRight className="ml-2 h-4 w-4" />
                        </Link>
                    </Button>
                </div>
            </section>
        </div>
    );
}
