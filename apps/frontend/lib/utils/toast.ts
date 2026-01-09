/**
 * Simple toast notification system.
 *
 * For production, consider using react-hot-toast or sonner.
 */

/**
 * Show a success toast notification.
 *
 * @param message - Success message to display
 */
function success(message: string): void {
  // Simple implementation using browser alert
  // TODO: Replace with proper toast library
  console.log("✅ Success:", message);
  if (typeof window !== "undefined") {
    // For now, just log to console. In production, use a toast library.
  }
}

/**
 * Show an error toast notification.
 *
 * @param message - Error message to display
 */
function error(message: string): void {
  // Simple implementation using browser alert
  // TODO: Replace with proper toast library
  console.error("❌ Error:", message);
  if (typeof window !== "undefined") {
    // For now, just log to console. In production, use a toast library.
  }
}

export const toast = {
  success,
  error,
};
