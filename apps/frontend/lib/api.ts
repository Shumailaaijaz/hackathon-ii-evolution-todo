/**
 * API client for communicating with the FastAPI backend.
 *
 * All functions handle JWT token authentication automatically.
 * Transforms backend snake_case fields to frontend camelCase.
 */

import type {
  ApiResponse,
  Task,
  TaskCreateRequest,
  TaskListParams,
  TaskUpdateRequest,
} from "./types";
import { getAuthToken } from "./auth-client";

// Base API URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Backend task format (snake_case).
 */
interface BackendTask {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

/**
 * Transform backend task to frontend format.
 */
function transformTask(backendTask: BackendTask): Task {
  return {
    id: backendTask.id,
    userId: backendTask.user_id,
    title: backendTask.title,
    description: backendTask.description,
    status: backendTask.status as Task["status"],
    createdAt: backendTask.created_at,
    updatedAt: backendTask.updated_at,
  };
}

/**
 * Make an authenticated API request.
 */
async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const token = await getAuthToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Merge with any additional headers from options
  if (options.headers) {
    const optionsHeaders = new Headers(options.headers);
    optionsHeaders.forEach((value, key) => {
      headers[key] = value;
    });
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Handle different response statuses
  if (!response.ok) {
    // Try to parse error response
    try {
      const errorData = await response.json();
      return errorData as ApiResponse<T>;
    } catch {
      // If parsing fails, return generic error
      return {
        success: false,
        data: null,
        error: {
          code: `HTTP_${response.status}`,
          message: `Request failed with status ${response.status}`,
        },
      };
    }
  }

  // Parse successful response
  const data = await response.json();
  return data as ApiResponse<T>;
}

/**
 * Get all tasks for the authenticated user.
 *
 * @param userId - The user's ID
 * @param params - Optional query parameters for filtering and sorting
 * @returns Promise with ApiResponse containing array of tasks
 */
export async function getTasks(
  userId: string,
  params?: TaskListParams
): Promise<ApiResponse<Task[]>> {
  const queryParams = new URLSearchParams();

  if (params?.status !== undefined) {
    queryParams.set("status", params.status);
  }
  if (params?.sort) {
    queryParams.set("sort", params.sort);
  }
  if (params?.order) {
    queryParams.set("order", params.order);
  }

  const query = queryParams.toString();
  const endpoint = `/api/${userId}/tasks${query ? `?${query}` : ""}`;

  const response = await fetchWithAuth<BackendTask[]>(endpoint);

  // Transform backend tasks to frontend format
  if (response.success && response.data) {
    return {
      ...response,
      data: response.data.map(transformTask),
    };
  }

  return response as ApiResponse<Task[]>;
}

/**
 * Get a single task by ID.
 *
 * @param userId - The user's ID
 * @param taskId - The task's ID (UUID)
 * @returns Promise with ApiResponse containing the task
 */
export async function getTask(
  userId: string,
  taskId: string
): Promise<ApiResponse<Task>> {
  const response = await fetchWithAuth<BackendTask>(`/api/${userId}/tasks/${taskId}`);

  // Transform backend task to frontend format
  if (response.success && response.data) {
    return {
      ...response,
      data: transformTask(response.data),
    };
  }

  return response as ApiResponse<Task>;
}

/**
 * Create a new task.
 *
 * @param userId - The user's ID
 * @param taskData - Task creation data (title, description)
 * @returns Promise with ApiResponse containing the created task
 */
export async function createTask(
  userId: string,
  taskData: TaskCreateRequest
): Promise<ApiResponse<Task>> {
  const response = await fetchWithAuth<BackendTask>(`/api/${userId}/tasks`, {
    method: "POST",
    body: JSON.stringify(taskData),
  });

  // Transform backend task to frontend format
  if (response.success && response.data) {
    return {
      ...response,
      data: transformTask(response.data),
    };
  }

  return response as ApiResponse<Task>;
}

/**
 * Update an existing task.
 *
 * @param userId - The user's ID
 * @param taskId - The task's ID (UUID)
 * @param taskData - Updated task data (title, description, status)
 * @returns Promise with ApiResponse containing the updated task
 */
export async function updateTask(
  userId: string,
  taskId: string,
  taskData: TaskUpdateRequest
): Promise<ApiResponse<Task>> {
  const response = await fetchWithAuth<BackendTask>(`/api/${userId}/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(taskData),
  });

  // Transform backend task to frontend format
  if (response.success && response.data) {
    return {
      ...response,
      data: transformTask(response.data),
    };
  }

  return response as ApiResponse<Task>;
}

/**
 * Toggle task completion status.
 *
 * @param userId - The user's ID
 * @param taskId - The task's ID (UUID)
 * @returns Promise with ApiResponse containing the updated task
 */
export async function toggleTask(
  userId: string,
  taskId: string
): Promise<ApiResponse<Task>> {
  const response = await fetchWithAuth<BackendTask>(`/api/${userId}/tasks/${taskId}/toggle`, {
    method: "PATCH",
  });

  // Transform backend task to frontend format
  if (response.success && response.data) {
    return {
      ...response,
      data: transformTask(response.data),
    };
  }

  return response as ApiResponse<Task>;
}

/**
 * Delete a task permanently.
 *
 * @param userId - The user's ID
 * @param taskId - The task's ID (UUID)
 * @returns Promise with ApiResponse containing success message
 */
export async function deleteTask(
  userId: string,
  taskId: string
): Promise<ApiResponse<{ message: string; task_id: string }>> {
  return fetchWithAuth(`/api/${userId}/tasks/${taskId}`, {
    method: "DELETE",
  });
}
