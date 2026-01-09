/**
 * TypeScript type definitions for the Todo application.
 *
 * These types define the structure for users, tasks, and API responses.
 * They must match the backend Pydantic schemas.
 */

/**
 * User information from Better Auth.
 */
export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Task status enumeration matching backend.
 */
export type TaskStatus = "pending" | "in_progress" | "completed";

/**
 * Task entity representing a todo item.
 */
export interface Task {
  id: string;  // UUID
  userId: string;  // user_id from backend
  title: string;
  description: string | null;
  status: TaskStatus;  // Changed from completed: boolean
  createdAt: string;  // created_at from backend
  updatedAt: string;  // updated_at from backend
}

/**
 * API response wrapper for all endpoints.
 *
 * Success responses have success=true and populated data.
 * Error responses have success=false and populated error.
 */
export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: {
    code: string;
    message: string;
  } | null;
}

/**
 * Request payload for creating a new task.
 */
export interface TaskCreateRequest {
  title: string;
  description?: string;
}

/**
 * Request payload for updating an existing task.
 * All fields are optional for partial updates.
 */
export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  status?: TaskStatus;  // Changed from completed
}

/**
 * Query parameters for listing tasks.
 */
export interface TaskListParams {
  status?: TaskStatus;  // Changed from completed
  sort?: "created_at" | "updated_at" | "title";
  order?: "asc" | "desc";
}

/**
 * Better Auth session information.
 */
export interface Session {
  user: User;
  token: string;
  expiresAt: string;
}

/**
 * Authentication state.
 */
export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  session: Session | null;
  isLoading: boolean;
}

/**
 * Form data for user signup.
 */
export interface SignupFormData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

/**
 * Form data for user signin.
 */
export interface SigninFormData {
  email: string;
  password: string;
}
