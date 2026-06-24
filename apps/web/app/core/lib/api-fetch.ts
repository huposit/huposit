const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function getApi<T>(path: string): Promise<T> {
    const response = await fetch(new URL(path, API_BASE_URL));
    if (!response.ok)
        throw new Error(`HTTP ${response.status}`);
    return (await response.json()) as T;
}

