/**
 * Better Auth client configuration.
 *
 * Provides authentication state management and session handling
 * for the frontend application.
 */

import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client instance.
 *
 * Configuration:
 * - baseURL: Points to the backend API authentication endpoints
 * - credentials: Include credentials (cookies) in requests
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

/**
 * Get the current JWT token from Better Auth session.
 *
 * @returns JWT token string or null if not authenticated
 */
export async function getAuthToken(): Promise<string | null> {
  try {
    // Get the current session from Better Auth
    const session = await authClient.getSession();

    if (!session?.data?.session?.token) {
      return null;
    }

    return session.data.session.token;
  } catch (error) {
    console.error("Failed to get auth token:", error);
    return null;
  }
}

/**
 * Get the current authenticated user.
 *
 * @returns User object or null if not authenticated
 */
export async function getCurrentUser() {
  try {
    const session = await authClient.getSession();
    return session?.data?.user ?? null;
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
 * @returns Sign in result
 */
export async function signIn(email: string, password: string) {
  return authClient.signIn.email({
    email,
    password,
  });
}

/**
 * Sign up with email and password.
 *
 * @param name - User's display name
 * @param email - User's email address
 * @param password - User's password
 * @returns Sign up result
 */
export async function signUp(name: string, email: string, password: string) {
  return authClient.signUp.email({
    name,
    email,
    password,
  });
}

/**
 * Sign out the current user.
 */
export async function signOut() {
  return authClient.signOut();
}

/**
 * Check if the user is authenticated.
 *
 * @returns true if authenticated, false otherwise
 */
export async function isAuthenticated(): Promise<boolean> {
  const session = await authClient.getSession();
  return !!session?.data?.session;
}
