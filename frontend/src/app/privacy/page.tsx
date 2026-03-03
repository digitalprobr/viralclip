import { Navbar } from "@/components/navbar";

export const metadata = { title: "Privacy Policy | AutoClip AI", description: "AutoClip AI Privacy Policy — how we collect, use, and protect your data." };

export default function PrivacyPage() {
    return (
        <div className="min-h-screen">
            <Navbar />
            <section className="pt-20 pb-24 px-4">
                <div className="mx-auto max-w-3xl">
                    <h1 className="text-4xl font-extrabold tracking-tight mb-2">Privacy Policy</h1>
                    <p className="text-muted-foreground mb-10">Last updated: March 1, 2026</p>

                    <div className="space-y-8 text-muted-foreground leading-relaxed text-sm">
                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">1. Information We Collect</h2>
                            <p className="mb-2">We collect information you provide directly:</p>
                            <ul className="list-disc list-inside space-y-1 pl-2">
                                <li><strong className="text-foreground">Account Data:</strong> Email address, username, and encrypted password when you register</li>
                                <li><strong className="text-foreground">Usage Data:</strong> YouTube URLs you submit, clips generated, and platform preferences</li>
                                <li><strong className="text-foreground">Payment Data:</strong> Billing information processed securely through Stripe (we never store card numbers)</li>
                                <li><strong className="text-foreground">Analytics:</strong> Page views, feature usage, and performance metrics</li>
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">2. How We Use Your Information</h2>
                            <ul className="list-disc list-inside space-y-1 pl-2">
                                <li>Provide and improve our video clipping services</li>
                                <li>Process your transactions and manage your account</li>
                                <li>Send service-related notifications and updates</li>
                                <li>Analyze usage patterns to enhance platform performance</li>
                                <li>Prevent fraud and ensure platform security</li>
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">3. Data Storage & Security</h2>
                            <p>Your data is stored on encrypted servers hosted within the EU. We use industry-standard security measures including TLS encryption, bcrypt password hashing, and regular security audits. Generated video clips are stored temporarily and automatically deleted after 30 days.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">4. Third-Party Services</h2>
                            <ul className="list-disc list-inside space-y-1 pl-2">
                                <li><strong className="text-foreground">Stripe:</strong> Payment processing</li>
                                <li><strong className="text-foreground">Google Gemini:</strong> AI video analysis (video URLs are processed temporarily)</li>
                                <li><strong className="text-foreground">YouTube API:</strong> Video downloading (subject to YouTube&apos;s Terms of Service)</li>
                                <li><strong className="text-foreground">Vercel/Docker:</strong> Application hosting</li>
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">5. Your Rights (GDPR)</h2>
                            <p className="mb-2">Under GDPR, you have the right to:</p>
                            <ul className="list-disc list-inside space-y-1 pl-2">
                                <li>Access your personal data</li>
                                <li>Rectify inaccurate information</li>
                                <li>Request deletion of your data</li>
                                <li>Data portability (export your data)</li>
                                <li>Object to processing</li>
                                <li>Withdraw consent at any time</li>
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">6. Cookies</h2>
                            <p>We use essential cookies for authentication (JWT session cookies) and optional analytics cookies. You can manage cookie preferences in your browser settings.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">7. Data Retention</h2>
                            <p>Account data is retained while your account is active. Generated clips are deleted after 30 days. Payment records are retained for 7 years as required by law. You can request full account deletion at any time.</p>
                        </div>

                        <div>
                            <h2 className="text-lg font-bold text-foreground mb-2">8. Contact</h2>
                            <p>For privacy-related inquiries, contact us at <a href="mailto:privacy@autoclipai.com" className="text-primary hover:underline">privacy@autoclipai.com</a>.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
