/**
 * React hook for authentication state management.
 *
 * Provides authentication state and methods for sign in, sign up, and sign out.
 */

"use client";

import { useEffect, useState } from "react";
import {
  authClient,
  getCurrentUser,
  isAuthenticated,
  signIn as authSignIn,
  signOut as authSignOut,
  signUp as authSignUp,
} from "../auth-client";
import type { User, AuthState, Session } from "../types";

/**
 * Authentication hook.
 *
 * @returns Authentication state and methods
 */
export function useAuth(): AuthState & {
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (name: string, email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  refetch: () => Promise<void>;
} {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    session: null,
    isLoading: true,
  });

  /**
   * Fetch and update authentication state.
   */
  const fetchAuthState = async () => {
    setAuthState((prev) => ({ ...prev, isLoading: true }));

    try {
      const authenticated = await isAuthenticated();
      const user = authenticated ? await getCurrentUser() : null;
      const sessionData = authenticated ? await authClient.getSession() : null;

      // Extract session info and create our Session type
      const session: Session | null = sessionData?.data?.user
        ? {
            user: {
              id: sessionData.data.user.id,
              email: sessionData.data.user.email,
              name: sessionData.data.user.name,
              createdAt: new Date(sessionData.data.user.createdAt).toISOString(),
              updatedAt: new Date(sessionData.data.user.updatedAt).toISOString(),
            },
            token: (sessionData.data.session as any)?.token || "",
            expiresAt: (sessionData.data.session as any)?.expiresAt || "",
          }
        : null;

      setAuthState({
        isAuthenticated: authenticated,
        user: user as User | null,
        session,
        isLoading: false,
      });
    } catch (error) {
      console.error("Failed to fetch auth state:", error);
      setAuthState({
        isAuthenticated: false,
        user: null,
        session: null,
        isLoading: false,
      });
    }
  };

  /**
   * Sign in with email and password.
   */
  const signIn = async (email: string, password: string) => {
    try {
      await authSignIn(email, password);
      await fetchAuthState();
    } catch (error) {
      console.error("Sign in failed:", error);
      throw error;
    }
  };

  /**
   * Sign up with name, email, and password.
   */
  const signUp = async (name: string, email: string, password: string) => {
    try {
      await authSignUp(name, email, password);
      await fetchAuthState();
    } catch (error) {
      console.error("Sign up failed:", error);
      throw error;
    }
  };

  /**
   * Sign out the current user.
   */
  const signOut = async () => {
    try {
      await authSignOut();
      await fetchAuthState();
    } catch (error) {
      console.error("Sign out failed:", error);
      throw error;
    }
  };

  // Fetch auth state on mount
  useEffect(() => {
    fetchAuthState();
  }, []);

  return {
    ...authState,
    signIn,
    signUp,
    signOut,
    refetch: fetchAuthState,
  };
}
