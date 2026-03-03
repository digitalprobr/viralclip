import { Navbar } from "@/components/navbar";

export const metadata = { title: "Terms of Service | AutoClip AI", description: "AutoClip AI Terms of Service — the rules and guidelines for using our platform." };

export default function TermsPage() {
    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-3xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-2">Terms of Service</h1>
                    <p className="text-muted-foreground mb-10">Last updated: March 1, 2026</p>

                    <div className="space-y-8 text-muted-foreground leading-relaxed text-sm">
                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">1. Acceptance of Terms</h2>
                            <p>By accessing or using AutoClip AI (&quot;the Service&quot;), you agree to be bound by these Terms of Service. If you do not agree, please do not use the Service.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">2. Description of Service</h2>
                            <p>AutoClip AI is an AI-powered video clipping platform that transforms long-form videos into short-form viral clips. The Service includes video analysis, face tracking, subtitle generation, and multi-platform export capabilities.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">3. Account Registration</h2>
                            <ul className="list-disc list-inside space-y-1 pl-2">
                                <li>You must provide accurate and complete information during registration</li>
                                <li>You are responsible for maintaining the security of your account credentials</li>
                                <li>You must be at least 18 years old to create an account</li>
                                <li>One person may not maintain more than one free account</li>
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">4. Acceptable Use</h2>
                            <p className="mb-2">You agree NOT to:</p>
                            <ul className="list-disc list-inside space-y-1 pl-2">
                                <li>Use the Service for any illegal purposes</li>
                                <li>Upload or process content you do not have rights to use</li>
                                <li>Attempt to bypass credit limits or usage restrictions</li>
                                <li>Reverse engineer, decompile, or disassemble any part of the Service</li>
                                <li>Use the Service to generate harmful, misleading, or hateful content</li>
                                <li>Share your account credentials with others</li>
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">5. Content & Copyright</h2>
                            <p>You are responsible for ensuring you have the necessary rights to process any video through our Service. AutoClip AI does not claim ownership of content you create. Generated clips are your property, but you are responsible for compliance with copyright laws and platform terms.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">6. Credits & Billing</h2>
                            <ul className="list-disc list-inside space-y-1 pl-2">
                                <li>Free accounts receive 50 credits upon registration</li>
                                <li>Credits are consumed when processing videos (10 credits per video)</li>
                                <li>Paid plans renew automatically unless cancelled</li>
                                <li>Refunds are available within 14 days of purchase if no credits have been used</li>
                                <li>Unused credits do not roll over between billing periods</li>
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">7. Service Availability</h2>
                            <p>We strive for 99.9% uptime but do not guarantee uninterrupted access. We reserve the right to suspend the Service for maintenance, updates, or security purposes. We will provide advance notice when possible.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">8. Limitation of Liability</h2>
                            <p>AutoClip AI shall not be liable for any indirect, incidental, special, or consequential damages arising from your use of the Service. Our total liability shall not exceed the amount you paid for the Service in the 12 months preceding the claim.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">9. Termination</h2>
                            <p>We may suspend or terminate your account if you violate these Terms. You may delete your account at any time. Upon termination, your data will be deleted within 30 days.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">10. Contact</h2>
                            <p>For questions about these Terms, contact us at <a href="mailto:legal@autoclipai.com" className="text-primary hover:underline">legal@autoclipai.com</a>.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
