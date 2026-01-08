/**
 * Authentication Provider component.
 *
 * Wraps the application and provides Better Auth context.
 */

"use client";

import { ReactNode } from "react";

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * AuthProvider component.
 *
 * This component wraps the application and initializes Better Auth.
 * It should be placed at the root of the application in the layout.
 */
export function AuthProvider({ children }: AuthProviderProps) {
  return <>{children}</>;
}
