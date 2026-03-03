"use client";
import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Mail, MessageSquare, Send, MapPin, Globe, Loader2, CheckCircle2 } from "lucide-react";

export default function ContactPage() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [sent, setSent] = useState(false);
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setLoading(true);
        await new Promise((r) => setTimeout(r, 1000));
        setSent(true);
        setLoading(false);
    }

    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-3xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-4">Contact <span className="text-gradient">Us</span></h1>
                    <p className="text-muted-foreground text-lg mb-10">Have questions? We&apos;d love to hear from you.</p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                        {[
                            { icon: Mail, title: "Email", desc: "support@autoclipai.com", href: "mailto:support@autoclipai.com" },
                            { icon: Globe, title: "Social", desc: "@autoclipai", href: "#" },
                            { icon: MapPin, title: "Location", desc: "Remote · Global", href: "#" },
                        ].map((item, i) => (
                            <Card key={i} className="bg-card border-border">
                                <CardContent className="p-6 text-center">
                                    <item.icon className="h-6 w-6 text-primary mx-auto mb-3" />
                                    <h3 className="font-semibold text-sm">{item.title}</h3>
                                    <a href={item.href} className="text-xs text-primary hover:underline">{item.desc}</a>
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    {sent ? (
                        <Card className="bg-card/80 border-primary/20">
                            <CardContent className="p-12 text-center">
                                <CheckCircle2 className="h-12 w-12 text-primary mx-auto mb-4" />
                                <h2 className="text-2xl font-bold mb-2">Message Sent!</h2>
                                <p className="text-muted-foreground">We&apos;ll get back to you within 24 hours.</p>
                            </CardContent>
                        </Card>
                    ) : (
                        <Card className="bg-card/80 border-border">
                            <CardContent className="p-8">
                                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                                    <MessageSquare className="h-5 w-5 text-primary" /> Send a Message
                                </h2>
                                <form onSubmit={handleSubmit} className="space-y-4">
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                        <div><label className="text-sm font-medium mb-1 block">Name</label><Input placeholder="Your name" value={name} onChange={(e) => setName(e.target.value)} required /></div>
                                        <div><label className="text-sm font-medium mb-1 block">Email</label><Input type="email" placeholder="you@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required /></div>
                                    </div>
                                    <div><label className="text-sm font-medium mb-1 block">Message</label><textarea placeholder="How can we help?" value={message} onChange={(e) => setMessage(e.target.value)} required rows={5} className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" /></div>
                                    <Button type="submit" className="w-full h-12 bg-primary text-primary-foreground" disabled={loading}>
                                        {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Sending...</> : <><Send className="mr-2 h-4 w-4" /> Send Message</>}
                                    </Button>
                                </form>
                            </CardContent>
                        </Card>
                    )}
                </div>
            </section>
        </div>
    );
}
