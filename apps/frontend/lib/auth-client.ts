/**
 * Authentication client for JWT-based authentication.
 *
 * Provides authentication state management and session handling
 * for the frontend application using custom backend JWT API.
 */

// Base API URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Local storage keys
const TOKEN_KEY = "auth_token";
const USER_KEY = "auth_user";

/**
 * Backend user response (snake_case from API)
 */
interface BackendUser {
  id: string;
  email: string;
  created_at: string;
  is_active: boolean;
}

/**
 * Authentication response from backend
 */
interface AuthResponse {
  success: boolean;
  message: string;
  data: {
    user: BackendUser;
    token: string;
    token_type: string;
    expires_in: number;
  };
}

/**
 * Get the current JWT token from local storage.
 *
 * @returns JWT token string or null if not authenticated
 */
export async function getAuthToken(): Promise<string | null> {
  if (typeof window === "undefined") {
    return null;
  }

  try {
    const token = localStorage.getItem(TOKEN_KEY);
    return token;
  } catch (error) {
    console.error("Failed to get auth token:", error);
    return null;
  }
}

/**
 * Get the current authenticated user from local storage.
 *
 * @returns User object or null if not authenticated
 */
export async function getCurrentUser() {
  if (typeof window === "undefined") {
    return null;
  }

  try {
    const userJson = localStorage.getItem(USER_KEY);
    if (!userJson) {
      return null;
    }
    const backendUser = JSON.parse(userJson) as BackendUser;

    // Transform to frontend User format (camelCase)
    return {
      id: backendUser.id,
      email: backendUser.email,
      name: backendUser.email.split('@')[0], // Use email prefix as name
      createdAt: backendUser.created_at,
      updatedAt: backendUser.created_at, // Backend doesn't track updated_at for users
    };
  } catch (error) {
    console.error("Failed to get current user:", error);
    return null;
  }
}

/**
 * Sign in with email and password.
 *
 * @param email - User's email address
 * @param password - User's password
 * @returns Sign in result with user and token
 */
export async function signIn(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/signin`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (data.success && data.data.token) {
    // Store token and user in local storage
    localStorage.setItem(TOKEN_KEY, data.data.token);
    localStorage.setItem(USER_KEY, JSON.stringify(data.data.user));
  }

  return data;
}

/**
 * Sign up with email and password.
 *
 * @param email - User's email address
 * @param password - User's password
 * @returns Sign up result with user and token
 */
export async function signUp(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (data.success && data.data.token) {
    // Store token and user in local storage
    localStorage.setItem(TOKEN_KEY, data.data.token);
    localStorage.setItem(USER_KEY, JSON.stringify(data.data.user));
  }

  return data;
}

/**
 * Sign out the current user.
 */
export async function signOut() {
  if (typeof window === "undefined") {
    return;
  }

  try {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  } catch (error) {
    console.error("Failed to sign out:", error);
  }
}

/**
 * Check if the user is authenticated.
 *
 * @returns true if authenticated, false otherwise
 */
export async function isAuthenticated(): Promise<boolean> {
  const token = await getAuthToken();
  return !!token;
}
