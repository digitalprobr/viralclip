const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080/api/v1";

export interface ClipRequest {
    url: string;
    preferred_engine?: string;
    num_clips?: number;
}

export interface TaskResponse {
    task_id: string;
    message: string;
    status: string;
}

export interface TaskStatus {
    task_id: string;
    task_status: string;
    result?: {
        status: string;
        clips_dir: string;
        effects_plan_used: boolean;
        seo_generated: boolean;
    };
    error?: string;
}

export async function submitClipJob(data: ClipRequest): Promise<TaskResponse> {
    const res = await fetch(`${API_BASE_URL}/clip`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`API Error: ${res.statusText}`);
    return res.json();
}

export async function getTaskStatus(taskId: string): Promise<TaskStatus> {
    const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`);
    if (!res.ok) throw new Error(`API Error: ${res.statusText}`);
    return res.json();
}

export async function checkHealth(): Promise<{ status: string; service: string }> {
    const res = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);
    if (!res.ok) throw new Error("API unreachable");
    return res.json();
}
