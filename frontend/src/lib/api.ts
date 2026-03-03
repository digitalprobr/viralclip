/**
 * ViralClip API Client — Typed fetch wrapper.
 * Handles auth tokens, error handling, and SSE streaming.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

// ── Types ──────────────────────────────────────────────

export type User = {
    id: number;
    email: string;
    username: string | null;
    name: string | null;
    email_verified: boolean;
    credits: number;
};

export type AuthResponse = {
    message: string;
    purpose: string | null;
};

export type TokenResponse = {
    access_token: string;
    token_type: string;
    user: User;
};

export type JobResponse = {
    id: number;
    celery_task_id: string | null;
    url: string;
    engine: string;
    status: string;
    progress: number;
    current_step: string | null;
    result_path: string | null;
    error_message: string | null;
    credits_used: number;
    created_at: string;
    completed_at: string | null;
};

export type ClipFile = {
    name: string;
    platform: string;
    url: string;
    size: number;
};

export type ProgressEvent = {
    progress: number;
    step: string;
    status: string;
    logs?: string[];
    result?: Record<string, unknown>;
    error?: string;
};

// ── Auth helpers ──────────────────────────────────────────

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
    accessToken = token;
    if (token) {
        localStorage.setItem("viralclip_token", token);
    } else {
        localStorage.removeItem("viralclip_token");
    }
}

export function getAccessToken(): string | null {
    if (accessToken) return accessToken;
    if (typeof window !== "undefined") {
        accessToken = localStorage.getItem("viralclip_token");
    }
    return accessToken;
}

function authHeaders(): HeadersInit {
    const token = getAccessToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
}

// ── Auth API ──────────────────────────────────────────────

export async function signup(data: {
    username: string;
    email: string;
    password: string;
    confirm_password: string;
}): Promise<TokenResponse> {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        credentials: "include",
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || res.statusText);
    }
    return res.json();
}

export async function login(email: string, password: string): Promise<TokenResponse> {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include",
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || res.statusText);
    }
    return res.json();
}

export async function registerOrLogin(email: string): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
    return res.json();
}

export async function verifyMagicLink(token: string): Promise<TokenResponse> {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/verify?token=${token}`, {
        credentials: "include",
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Invalid magic link");
    return res.json();
}

export async function getMe(): Promise<User | null> {
    const token = getAccessToken();
    if (!token) return null;
    try {
        const res = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
            headers: authHeaders(),
            credentials: "include",
        });
        if (!res.ok) return null;
        return res.json();
    } catch {
        return null;
    }
}

export async function logout(): Promise<void> {
    await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
        method: "POST",
        credentials: "include",
    }).catch(() => { });
    setAccessToken(null);
}

// ── Jobs API ──────────────────────────────────────────────

export async function submitClipJob(data: {
    url: string;
    preferred_engine?: string;
    num_clips?: number;
}): Promise<{ job_id: number; task_id: string; credits_remaining: number }> {
    const res = await fetch(`${API_BASE_URL}/api/v1/clip`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data),
        credentials: "include",
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || res.statusText);
    }
    return res.json();
}

export async function listJobs(): Promise<JobResponse[]> {
    const res = await fetch(`${API_BASE_URL}/api/v1/jobs`, {
        headers: authHeaders(),
        credentials: "include",
    });
    if (!res.ok) return [];
    return res.json();
}

export async function getTaskStatus(taskId: string) {
    const res = await fetch(`${API_BASE_URL}/api/v1/tasks/${taskId}`);
    if (!res.ok) throw new Error(res.statusText);
    return res.json();
}

export async function getClipFiles(jobId: number): Promise<{ files: ClipFile[] }> {
    const res = await fetch(`${API_BASE_URL}/api/v1/clips/${jobId}/files`, {
        headers: authHeaders(),
        credentials: "include",
    });
    if (!res.ok) return { files: [] };
    return res.json();
}

// ── SSE Progress ──────────────────────────────────────────

export function subscribeToProgress(
    taskId: string,
    onEvent: (data: ProgressEvent) => void,
    onDone?: () => void,
): () => void {
    const url = `${API_BASE_URL}/api/v1/tasks/${taskId}/stream`;
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
        const data: ProgressEvent = JSON.parse(event.data);
        onEvent(data);
        if (data.status === "SUCCESS" || data.status === "FAILURE") {
            eventSource.close();
            onDone?.();
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        onDone?.();
    };

    return () => eventSource.close();
}

// ── Health ────────────────────────────────────────────────

export async function checkHealth(): Promise<boolean> {
    try {
        const res = await fetch(`${API_BASE_URL}/health`);
        return res.ok;
    } catch {
        return false;
    }
}

export function getFileUrl(path: string): string {
    return `${API_BASE_URL}${path}`;
}
