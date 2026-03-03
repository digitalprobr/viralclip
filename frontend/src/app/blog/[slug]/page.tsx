"use client";

import { use } from "react";
import { Navbar } from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { ArrowLeft, ArrowRight, Clock, Tag, User, BookOpen } from "lucide-react";
import Link from "next/link";
import { blogArticles } from "../data";

function MarkdownContent({ content }: { content: string }) {
    const blocks = content.split("\n\n");

    return (
        <div className="space-y-4">
            {blocks.map((block, i) => {
                const trimmed = block.trim();

                // Headings
                if (trimmed.startsWith("#### ")) {
                    return <h4 key={i} className="text-lg font-bold mt-6 mb-2 text-foreground">{trimmed.replace("#### ", "")}</h4>;
                }
                if (trimmed.startsWith("### ")) {
                    return <h3 key={i} className="text-xl font-bold mt-8 mb-3 text-foreground">{trimmed.replace("### ", "")}</h3>;
                }
                if (trimmed.startsWith("## ")) {
                    return <h2 key={i} className="text-2xl font-bold mt-10 mb-4 text-foreground">{trimmed.replace("## ", "")}</h2>;
                }

                // Tables
                if (trimmed.startsWith("| ")) {
                    const lines = trimmed.split("\n").filter(l => l.trim().length > 0);
                    const headerLine = lines[0];
                    const bodyLines = lines.filter((_, idx) => idx > 0 && !lines[idx].match(/^\|\s*[-:]+/));

                    const parseCells = (line: string) => line.split("|").filter(Boolean).map(c => c.trim());
                    const headers = parseCells(headerLine);

                    return (
                        <div key={i} className="overflow-x-auto my-6 rounded-lg border border-border">
                            <table className="w-full text-sm">
                                <thead className="bg-card/80">
                                    <tr>
                                        {headers.map((cell, j) => (
                                            <th key={j} className="text-left p-3 font-semibold text-foreground border-b border-border">{cell}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {bodyLines.map((row, ri) => {
                                        const cells = parseCells(row);
                                        return (
                                            <tr key={ri} className="border-b border-border/30 hover:bg-card/30">
                                                {cells.map((cell, ci) => (
                                                    <td key={ci} className="p-3 text-muted-foreground">{cell}</td>
                                                ))}
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                    );
                }

                // Unordered lists
                if (trimmed.startsWith("- ")) {
                    const items = trimmed.split("\n").filter(l => l.startsWith("- "));
                    return (
                        <ul key={i} className="space-y-2 my-4 pl-1">
                            {items.map((item, j) => {
                                const text = item.replace("- ", "");
                                const rendered = text
                                    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-foreground font-semibold">$1</strong>');
                                return (
                                    <li key={j} className="flex items-start gap-3 text-sm text-muted-foreground">
                                        <span className="text-primary mt-1.5 text-xs">●</span>
                                        <span dangerouslySetInnerHTML={{ __html: rendered }} />
                                    </li>
                                );
                            })}
                        </ul>
                    );
                }

                // Ordered lists
                if (trimmed.match(/^\d+\.\s/)) {
                    const items = trimmed.split("\n").filter(l => l.match(/^\d+\.\s/));
                    return (
                        <ol key={i} className="space-y-2 my-4 pl-1">
                            {items.map((item, j) => {
                                const text = item.replace(/^\d+\.\s*/, "");
                                const rendered = text
                                    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-foreground font-semibold">$1</strong>');
                                return (
                                    <li key={j} className="flex items-start gap-3 text-sm text-muted-foreground">
                                        <span className="text-primary font-bold mt-0.5 text-xs min-w-[18px]">{j + 1}.</span>
                                        <span dangerouslySetInnerHTML={{ __html: rendered }} />
                                    </li>
                                );
                            })}
                        </ol>
                    );
                }

                // Code blocks
                if (trimmed.startsWith("```")) {
                    const code = trimmed.replace(/```\w*\n?/, "").replace(/```$/, "");
                    return (
                        <pre key={i} className="bg-card border border-border rounded-lg p-4 my-4 overflow-x-auto">
                            <code className="text-sm text-primary font-mono whitespace-pre">{code}</code>
                        </pre>
                    );
                }

                // Regular paragraphs with bold text
                if (trimmed.length === 0) return null;
                const rendered = trimmed
                    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-foreground font-semibold">$1</strong>');
                return (
                    <p key={i} className="text-muted-foreground leading-relaxed text-sm" dangerouslySetInnerHTML={{ __html: rendered }} />
                );
            })}
        </div>
    );
}

export default function BlogArticlePage({ params }: { params: Promise<{ slug: string }> }) {
    const { slug } = use(params);

    const article = blogArticles.find((a) => a.slug === slug);
    if (!article) {
        return (
            <div className="min-h-screen">
                <Navbar />
                <div className="pt-20 text-center">
                    <h1 className="text-2xl font-bold">Article not found</h1>
                    <Link href="/blog" className="text-primary hover:underline mt-4 block">Back to Blog</Link>
                </div>
            </div>
        );
    }

    const related = blogArticles
        .filter((a) => a.slug !== slug && a.category === article.category)
        .slice(0, 3);

    return (
        <div className="min-h-screen">
            <Navbar />

            {/* Article Header */}
            <section className="pt-20 pb-8 px-4">
                <div className="mx-auto max-w-3xl">
                    <Link href="/blog" className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors mb-6">
                        <ArrowLeft className="h-4 w-4" />
                        Back to Blog
                    </Link>

                    <div className="flex items-center gap-3 mb-4">
                        <span className="inline-flex items-center gap-1 text-xs font-medium text-primary bg-primary/10 px-3 py-1 rounded-full">
                            <Tag className="h-3 w-3" />
                            {article.category}
                        </span>
                        <span className="flex items-center gap-1 text-xs text-muted-foreground">
                            <Clock className="h-3 w-3" />
                            {article.readTime} read
                        </span>
                    </div>

                    <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-4">
                        {article.title}
                    </h1>

                    <p className="text-lg text-muted-foreground mb-6 leading-relaxed">
                        {article.excerpt}
                    </p>

                    <div className="flex items-center gap-3 pb-8 border-b border-border/50">
                        <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                            <User className="h-4 w-4 text-primary" />
                        </div>
                        <div>
                            <p className="text-sm font-medium">{article.author}</p>
                            <p className="text-xs text-muted-foreground">
                                {new Date(article.date).toLocaleDateString("en-US", {
                                    month: "long",
                                    day: "numeric",
                                    year: "numeric",
                                })}
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Article Content */}
            <section className="px-4 pb-16">
                <div className="mx-auto max-w-3xl">
                    <MarkdownContent content={article.content} />
                </div>
            </section>

            {/* CTA */}
            <section className="px-4 pb-16">
                <div className="mx-auto max-w-3xl bg-gradient-to-r from-primary/10 to-emerald-500/10 border border-primary/20 rounded-2xl p-8 text-center">
                    <h3 className="text-xl font-bold mb-3">Start Creating Viral Clips Today</h3>
                    <p className="text-muted-foreground mb-6">
                        50 free credits. No credit card required.
                    </p>
                    <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90" asChild>
                        <Link href="/auth/register">
                            Get Started Free <ArrowRight className="ml-2 h-4 w-4" />
                        </Link>
                    </Button>
                </div>
            </section>

            {/* Related Articles */}
            {related.length > 0 && (
                <section className="px-4 pb-24">
                    <div className="mx-auto max-w-3xl">
                        <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                            <BookOpen className="h-5 w-5 text-primary" />
                            Related Articles
                        </h3>
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            {related.map((r) => (
                                <Link key={r.slug} href={`/blog/${r.slug}`} className="block">
                                    <div className="bg-card border border-border rounded-xl p-4 hover:border-primary/50 transition-all h-full">
                                        <span className="text-xs text-primary">{r.category}</span>
                                        <h4 className="font-semibold text-sm mt-1 line-clamp-2 hover:text-primary transition-colors">
                                            {r.title}
                                        </h4>
                                        <p className="text-xs text-muted-foreground mt-2">{r.readTime}</p>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    </div>
                </section>
            )}
        </div>
    );
}
